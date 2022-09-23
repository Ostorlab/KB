Cross-site-scripting (XSS) vulnerabilities occur when unsanitized user-controlled input is served to user.

XSS vulnerabilities bypasses same-Origin-Policy, which is a core principal of web security. SOP ensures that a page from `http://evil.com` can't access the content of a page from `http://bank.com`.

XSS are commonly separated into 3 familities

*   **Reflected:** the user-controlled input is directly reflected in the page response
*   **Stored:** the user-controled input is stored on the server-side, for instance in a database, and is later returned to user
*   **DOM-based:** the user-controlled input is injected on the client-side to the DOM, triggering the injection of malicious JavaScript

XSS vulnerabilities allow an attacker to perform a variety of malcious actions, like exfiltration of personal data, including user session or account information; perform actions on behalf of the user.