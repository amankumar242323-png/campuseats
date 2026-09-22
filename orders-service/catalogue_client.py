import os
import random
import time

import requests


class CatalogueUnavailable(Exception):
    pass


class ItemUnavailable(Exception):
    pass


class CatalogueItemNotFound(Exception):
    pass


class CatalogueRejected(Exception):
    pass


def get_config():
    return {
        "base_url": os.environ.get(
            "CATALOGUE_URL",
            "http://127.0.0.1:8081"
        ).rstrip("/"),

        "timeout": float(
            os.environ.get(
                "CATALOGUE_TIMEOUT",
                "2.0"
            )
        ),

        "max_attempts": int(
            os.environ.get(
                "CATALOGUE_MAX_ATTEMPTS",
                "3"
            )
        ),

        "base_delay": float(
            os.environ.get(
                "CATALOGUE_BASE_DELAY",
                "0.5"
            )
        )
    }


def check_item(item_id: int):
    config = get_config()

    url = (
        f"{config['base_url']}"
        f"/menu-items/{item_id}"
    )

    for attempt in range(config["max_attempts"]):

        try:
            response = requests.get(
                url,
                timeout=config["timeout"]
            )

            # 404 is a business result.
            # Do not retry it.
            if response.status_code == 404:
                raise CatalogueItemNotFound(
                    f"Menu item {item_id} does not exist."
                )

            # Other 4xx responses are also not retryable.
            if 400 <= response.status_code < 500:
                raise CatalogueRejected(
                    f"Catalogue rejected request with "
                    f"status {response.status_code}."
                )

            # Successful response.
            if response.status_code == 200:
                data = response.json()

                if not data.get("available", False):
                    raise ItemUnavailable(
                        f"Menu item {item_id} is unavailable."
                    )

                return data

            # 5xx → retry
            if response.status_code >= 500:
                raise CatalogueUnavailable(
                    f"Catalogue returned "
                    f"{response.status_code}."
                )

            # Any unexpected status
            raise CatalogueUnavailable(
                f"Unexpected catalogue status "
                f"{response.status_code}."
            )

        except (
            CatalogueItemNotFound,
            CatalogueRejected,
            ItemUnavailable
        ):
            # Business/client outcomes are never retried.
            raise

        except (
            CatalogueUnavailable,
            requests.exceptions.RequestException
        ):
            # Retry only when attempts remain.
            if attempt == config["max_attempts"] - 1:
                raise CatalogueUnavailable(
                    "Catalogue service is unavailable "
                    "after all retry attempts."
                )

            wait = (
                config["base_delay"] * (2 ** attempt)
                + random.uniform(0, 0.25)
            )

            time.sleep(wait)