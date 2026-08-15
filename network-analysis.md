# Network Analysis

## Website Analyzed

**Website:** YouTube (`m.youtube.com`)

The website was opened in Google Chrome and analyzed using **DevTools → Network**.

## Network Setup

* Browser: Google Chrome
* DevTools panel: Network
* Disable cache: Enabled
* Throttling: No throttling
* Page was reloaded with the Network panel open

## Results

* **Total requests:** 231
* **Total resources:** 21.9 MB
* **Data transferred:** 18.2 MB
* **Page load finish:** 4.4 minutes
* **Slowest resource:** `m.youtube.com`
* **Slowest resource time:** 1.12 seconds

## Slowest Resource

After sorting the Network table by the **Time** column, the slowest resource visible at the top was:

**Resource:** `m.youtube.com`
**Status:** `302`
**Type:** Document
**Size:** 88.0 kB
**Time:** 1.12 seconds

The resource took the longest time among the requests shown in the sorted Network table.

## 3xx / 4xx Responses

Several **302** responses were observed during the page load.

Examples visible in the Network panel include:

* `m.youtube.com` — 302
* `www.youtube.com` — 302
* `open.mp3` — 302
* `success.mp3` — 302
* `failure.mp3` — 302
* `no_input.mp3` — 302

A **302 Found** response indicates that the requested resource is temporarily redirected to another location.

**4xx responses:** No 4xx response was visible in the captured Network results.

## Observation

The Network panel showed **231 requests** during the page load. The browser transferred **18.2 MB** of data and loaded resources totaling **21.9 MB**. The slowest resource visible after sorting by time was the `m.youtube.com` document request, which took **1.12 seconds**.

The Network waterfall also showed multiple `302` redirect responses. These redirects indicate that some requested resources were temporarily redirected to another location.

## Conclusion

The Chrome DevTools Network panel provides a detailed view of how a webpage loads its resources. It shows the number of requests, transferred data, resource sizes, response status codes, and loading times. This analysis helped identify the slowest resource and observe HTTP redirects during the page load.
