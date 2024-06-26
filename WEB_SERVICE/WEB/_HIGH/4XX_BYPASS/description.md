
# 4XX-Bypass

The 4xx-bypass exploits refers to HTTP request fuzzing techniques that allow an attacker to bypass server-side restrictions and access unauthorized resources or perform malicious actions on an unauthorized web application. This can lead to unauthorized data access, privilege escalation, and other security risks.

=== "Python example"
  ```python
    import requests

    response = requests.get("http://www.some-url.com/unauthorized_path")

    '''if we have some unauthorized path that gets us a 403 code,
    we can try something like adding a query parameter to see if we can
    trick the server by exploiting some mistake.'''

    response = requests.get("http://www.some-url.com/unauthorized_path?debug=true")

    '''Might get us the resource we want'''
  ```