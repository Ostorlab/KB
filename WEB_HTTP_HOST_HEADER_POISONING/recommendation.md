Protection against Host header attacks will require multiple checks that depend on the application target architecture,
like support for virtual host, use of a reverse proxy, presence on certain cloud environment the support extra
routing headers.

The recommendations to protect against these attacks are:

* Avoid using `Host` header value in application logic.
* Implement a whitelist check of accepted values, this is commonly supported by most web frameworks.
* Disable host override headers, this depends on the intermediary components deployed in your architecture. Common places to check are reverse-proxies, Kubernetes ingress controllers.