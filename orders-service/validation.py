def validate_place_order(body):
    errors = []

    if not isinstance(body, dict):
        return [["body", "must be a JSON object"]]

    student_id = body.get("studentId")
    items = body.get("items")
    delivery_address_id = body.get("deliveryAddressId")
    payment_method_id = body.get("paymentMethodId")

    if not isinstance(student_id, int):
        errors.append(["studentId", "required integer"])

    if not isinstance(items, list) or len(items) == 0:
        errors.append(["items", "must be a non-empty list"])
    else:
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append([
                    f"items[{index}]",
                    "must be an object"
                ])
                continue

            item_id = item.get("itemId")
            qty = item.get("qty")

            if not isinstance(item_id, int):
                errors.append([
                    f"items[{index}].itemId",
                    "required integer"
                ])

            if not isinstance(qty, int) or qty <= 0:
                errors.append([
                    f"items[{index}].qty",
                    "must be a positive integer"
                ])

    if not isinstance(delivery_address_id, int) or delivery_address_id <= 0:
        errors.append([
            "deliveryAddressId",
            "must be a positive integer"
        ])

    if not isinstance(payment_method_id, int) or payment_method_id <= 0:
        errors.append([
            "paymentMethodId",
            "must be a positive integer"
        ])

    return errors