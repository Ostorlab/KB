To mitigate the risk of Server-Side Request Forgery (SSRF), treat any user-controlled or stored value that influences a server-side request destination as untrusted and constrain it before the outbound request is issued. Apply controls both at the persistence layer (where the value is stored) and at the sink (where the outbound connection originates), as defense in depth.

- __Allowlist destinations__: prefer an allowlist of permitted hosts/domains over a blocklist. Only allow schemes that are required (typically `https`), and reject all others.
- __Private/internal IP blocklist__: when a hostname or IP is supplied, resolve it and reject the request if the resolved address is private, loopback, link-local, reserved, or multicast (for example the cloud metadata address `169.254.169.254`).
- __DNS pinning__: resolve the hostname once and require the outbound connection to target the resolved IP, to prevent DNS-rebinding TOCTOU.
- __Re-enable host verification__: do not disable transport-level host verification (for example `StrictHostKeyChecking no` for ssh, or `verify=False` for TLS). Maintain a known_hosts / trust store allowlist for approved destinations.
- __Reject redirects__: do not follow HTTP redirects on the server-side request, or re-validate the destination after each redirect.
- __Timeouts and retries__: set an explicit, short timeout on the outbound request and avoid unbounded retries that amplify a timing/retry oracle.
- __Validate at the sink__: because the sink is the actual network egress point, re-validate the resolved host at the sink in addition to validation at persistence time.

Below are examples of secure server-side request construction on different popular frameworks:

=== "Python"
   ```Python
   import ipaddress
   import socket
   from urllib.parse import urlparse

   import requests
   from django.http import HttpResponse


   def _assert_safe_host(url: str) -> None:
       parsed = urlparse(url)
       host = parsed.hostname
       if parsed.scheme not in ("http", "https") or host is None:
           raise ValueError("Unsupported url.")
       try:
           ip = ipaddress.ip_address(socket.gethostbyname(host))
       except (ValueError, socket.gaierror) as e:
           raise ValueError("Unresolvable host.") from e
       if (
           ip.is_private
           or ip.is_loopback
           or ip.is_link_local
           or ip.is_reserved
           or ip.is_multicast
       ):
           raise ValueError("Destination resolves to a private/internal range.")

   def fetch(request):
       url = request.GET.get("url")
       _assert_safe_host(url)
       response = requests.get(url, timeout=5, allow_redirects=False)
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
  import java.net.HttpURLConnection;
  import java.net.URL;

  @SpringBootApplication
  public class MitigatedSsrfExample {
      public static void main(String[] args) {
          SpringApplication.run(MitigatedSsrfExample.class, args);
      }
  }

  @RestController
  class FetchController {

      @GetMapping("/fetch")
      public String fetch(@RequestParam String url) {
          // Mitigated: validate scheme/host before issuing the request.
          if (!isValidUrl(url)) {
              return "Invalid destination.";
          }
          try {
              HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
              conn.setInstanceFollowRedirects(false);
              conn.setConnectTimeout(5000);
              conn.setReadTimeout(5000);
              try (InputStream in = conn.getInputStream()) {
                  return new String(in.readAllBytes());
              }
          } catch (Exception e) {
              return "Error: " + e.getMessage();
          }
      }

      private boolean isValidUrl(String url) {
          try {
              java.net.URI uri = java.net.URI.create(url);
              return ("http".equals(uri.getScheme()) || "https".equals(uri.getScheme()))
                  && uri.getHost() != null
                  && !isPrivateHost(uri.getHost());
          } catch (Exception e) {
              return false;
          }
      }

      private boolean isPrivateHost(String host) {
          try {
              java.net.InetAddress addr = java.net.InetAddress.getByName(host);
              return addr.isSiteLocalAddress() || addr.isLoopbackAddress()
                  || addr.isLinkLocalAddress() || addr.isAnyLocalAddress();
          } catch (Exception e) {
              return true;
          }
      }
  }
  ```

=== "NodeJs"
  ```javascript
  const express = require('express');
  const axios = require('axios');
  const dns = require('dns');
  const ipaddr = require('ipaddr.js');

  const app = express();

  function assertSafeHost(url) {
      return new Promise((resolve, reject) => {
          const parsed = new URL(url);
          if (!['http:', 'https:'].includes(parsed.protocol) || !parsed.hostname) {
              return reject(new Error('Unsupported url.'));
          }
          dns.lookup(parsed.hostname, { all: true }, (err, addresses) => {
              if (err || addresses.length === 0) {
                  return reject(new Error('Unresolvable host.'));
              }
              for (const entry of addresses) {
                  const ip = ipaddr.parse(entry.address);
                  const range = ip.range();
                  if (['private', 'loopback', 'linkLocal', 'reserved', 'multicast'].includes(range)) {
                      return reject(new Error('Destination resolves to a private/internal range.'));
                  }
              }
              resolve();
          });
      });
  }

  app.get('/fetch', async (req, res) => {
      const url = req.query.url;
      try {
          await assertSafeHost(url);
          const response = await axios.get(url, {
              timeout: 5000,
              maxRedirects: 0,
          });
          res.send(response.data);
      } catch (error) {
          res.status(500).send('Error: ' + error.message);
      }
  });

  app.listen(3000);
  ```
