A cookie is considered secure when it has the appropriate security attributes, such as `Secure` and `HttpOnly`. 

- The `Secure` flag ensures that the cookie is only sent over HTTPS, protecting it from being transmitted over unencrypted channels.
- The `HttpOnly` flag mitigates the risk of Cross-Site Scripting (XSS) attacks by making the cookie inaccessible to JavaScript.
- The `SameSite` controls whether cookies are sent with cross-site requests, helping to prevent Cross-Site Request Forgery (CSRF). This attribute can be set to:

  - `Strict`: The cookie is not sent with cross-site requests.
  - `Lax`: The cookie is sent with top-level navigation but not with embedded resources.
  - `None`: The cookie is sent with all requests, but requires the Secure flag if the value is None.
  
- The `Expires` or `Max-Age` attribute defines the lifespan of the cookie, ensuring it does not persist longer than intended.
- The `Domain` and `Path` attributes restrict where the cookie is sent based on the domain and URL path, allowing for cookie sharing limitations within a specific subdomain or path.

Here’s an example of a secure cookie configuration:

```http request
Set-Cookie: id=a3fWa; Expires=Wed, 21 Oct 2015 07:28:00 GMT; Secure; HttpOnly
```