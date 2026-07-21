Server-Side Request Forgery (SSRF) is a vulnerability in which an attacker is able to influence the destination of outbound requests issued by the server-side application. When user-controlled input is used to construct the URL, host, or request target of a server-side request (directly or stored/indirectly through a background consumer), the application can be tricked into contacting internal services, cloud metadata endpoints, or other attacker-controlled hosts that are reachable from the server's network position but not from the attacker's.

The impact of SSRF depends on the server's network position and the request transport:

- __Internal reachability & port scanning__: the server-side request reaches internal hosts and ports that are not directly accessible to the attacker, providing an internal-reachability and port-scanning primitive.
- __Cloud metadata exposure__: when the server runs in a cloud environment, requests to the cloud metadata service (for example `http://169.254.169.254/`) can return instance credentials and configuration.
- __Credential exfiltration__: when ambient backend credentials travel with the forged request (for example via host-matched tokens or ssh keys), they can be delivered to an attacker-controlled destination.
- __Blind / stored / indirect variants__: the request is issued out-of-band from a background consumer rather than synchronously from the request handler, so the response is not directly returned to the attacker; the primitive is instead an internal-reach or timing/retry oracle.

The vulnerability is amplified when host verification is disabled (for example `StrictHostKeyChecking no`), when the host is not resolved and pinned (DNS rebinding TOCTOU), when there is no host/IP blocklist for private/internal ranges, and when retries and timeouts amplify a timing oracle.

Below are examples of vulnerable server-side request construction on different popular frameworks:

=== "Python"
   ```Python
   import requests
   from django.http import HttpResponse


   def fetch(request):
       # Vulnerable: the destination is taken verbatim from user input with no
       # scheme/host/IP validation or private-IP blocklist.
       url = request.GET.get("url")
       response = requests.get(url)
       return HttpResponse(response.content)
   ```

=== "Java"
  ```java
  import org.springframework.boot.SpringApplication;
  import org.springframework.boot.autoconfigure.SpringBootApplication;
  import org.springframework.web.bind.annotation.GetMapping;
  import org.springframework.web.bind.annotation.RequestParam;
  import org.springframework.web.bind.annotation.RestController;
  import java.io.InputStream;
  import java.net.URL;

  @SpringBootApplication
  public class SsrfExample {
      public static void main(String[] args) {
          SpringApplication.run(SsrfExample.class, args);
      }
  }

  @RestController
  class FetchController {

      @GetMapping("/fetch")
      public String fetch(@RequestParam String url) {
          // Vulnerable: user-controlled url is opened directly with no validation.
          try (InputStream in = new URL(url).openStream()) {
              return new String(in.readAllBytes());
          } catch (Exception e) {
              return "Error: " + e.getMessage();
          }
      }
  }
  ```

=== "NodeJs"
  ```javascript
  const express = require('express');
  const axios = require('axios');

  const app = express();

  app.get('/fetch', async (req, res) => {
      // Vulnerable: the attacker controls the destination with no validation.
      const url = req.query.url;
      try {
          const response = await axios.get(url);
          res.send(response.data);
      } catch (error) {
          res.status(500).send('Error: ' + error.message);
      }
  });

  app.listen(3000);
  ```
