
# 4xx-bypass Vulnerability

The 4xx-bypass exploits refer to HTTP request manipulation techniques that allow attackers to bypass server-side restrictions, enabling unauthorized access to resources or performing malicious actions on a web application. This can lead to unauthorized data access, privilege escalation, and the ability for unauthorized users to retrieve, create, update, or delete sensitive data.

=== "Python"
  ```python
    import requests

    response = requests.get("http://www.some-url.com/unauthorized_path")

    '''if we have some unauthorized path that gets us a 403 code,
    we can try something like adding a query parameter like "debug=true" to see if we can
    trick the server by exploiting some mistake.'''

    response = requests.get("http://www.some-url.com/unauthorized_path?debug=true")

    '''Might get us the resource we want'''
  ```
=== "JavaScript"
   ```javascript

      const express = require('express');
      const app = express();

      app.get('/vulnerable_path', (req, res) => {
        const queryParams = req.query;

        if (queryParams.debug && queryParams.debug === 'true') {
          // Logic that would usually require more rights
          res.send('Debug mode enabled: Performing privileged actions.');
        } else {
          res.send('Normal mode: Limited actions.');
        }
      });

      app.listen(3000, () => {
          console.log('Server is running on port 3000');
      });
   ```
=== "PHP"
   ```php
    <?php
    // Simple example of a PHP backend that forgot a debug conditional for debugging purposes

    if ($_SERVER['REQUEST_METHOD'] === 'GET' || $_SERVER['REQUEST_METHOD'] === 'POST') {
        $queryParams = $_GET; // Using $_GET to retrieve query parameters from the URL

        if (isset($queryParams['debug']) && $queryParams['debug'] === 'true') {
            // Logic that would usually require more rights
            echo 'Debug mode enabled: Performing privileged actions.';
        } else {
            echo 'Normal mode: Limited actions.';
        }
    }
    ?>
   ```