In general, cases, preventing XSS vulnerabilities requires 2-step protection:

* **Input validation:** user-controlled input should be validated to forbid all unauthorized characters, phone number
  For instance, only numbers; names should only contain alphabetical characters, etc.
* **Output encoding:** all input shown to the user is encoded correctly using proven standard API. Use of a safe
  template engines with native support for output encoding and secure defaults are highly recommended.
