**Secure Cookie Implementation**: A cookie is considered secure when it has the appropriate security attributes, such as `Secure` and `HttpOnly`. 

- The `Secure` flag ensures that the cookie is only sent over HTTPS, protecting it from being transmitted over unencrypted channels.
- The `HttpOnly` flag mitigates the risk of Cross-Site Scripting (XSS) attacks by making the cookie inaccessible to JavaScript.

Here’s an example of a secure cookie configuration:

```http request
Set-Cookie: id=a3fWa; Expires=Wed, 21 Oct 2015 07:28:00 GMT; Secure; HttpOnly