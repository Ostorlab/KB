In general cases, preventing XSS vulnerabilities requires a 2-step protection:

*   **Input validation:** user-controlled input should be validated to forbid all unauthorized characters, phone number should for instance only contain numbers; names should only contain alphabetical characters, etc.
*   **Output encoding:** all input shown to user is properly encoded using standard proven API. Use of safe template engines with native support for output encoding and secure defaults is highly recommended.