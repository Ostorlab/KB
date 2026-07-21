An open redirect vulnerability occurs when a web application redirects a user to a destination URL that is derived from attacker-controllable input without validating the target's host or scheme. The application issues an HTTP redirect (typically `302 Found` with a `Location` header) whose value is taken verbatim from the request, so an attacker can craft a URL that lands the victim on an external, attacker-controlled site.

Because the redirect is issued by the legitimate application — often right after an authenticated action such as a login, a SAML assertion consumer, or a `return_to`/`next`/`redirect`/`redirectUrl` parameter handling — the victim's browser trusts the hop and silently follows it, carrying the freshly created session and giving the phishing page the appearance of originating from the trusted origin.

Open redirects can materialize in different ways:

* **Unvalidated redirect parameter**: the application reads a `redirect`/`next`/`return_to`/`redirectUrl`/`RelayState`-embedded value and passes it straight to a redirect response without a host allowlist.
* **Protocol-relative redirect**: a value such as `//evil.com/path` is treated as a cross-origin navigation by the browser even though it has no explicit scheme.
* **Host-header derived redirect**: the redirect destination is built from the `Host` header or `X-Forwarded-Host` and therefore attacker-controllable.
* **Post-authentication redirect amplification**: the redirect fires only after a successful authentication step (e.g. a validated SAML response), turning an otherwise benign open redirect into a reliable phishing amplification of a legitimate authenticated session.

Open redirects are abused primarily for:

* **Phishing**: redirecting an authenticated user from a trusted domain to an attacker-controlled credential-harvesting page that inherits the visual trust of the legitimate origin.
* **OAuth / SSO token theft**: laundering authorization `code`/`state`/`session` parameters through the trusted redirect to an attacker endpoint.
* **Bypass of URL-based allowlists**: chained with SSRF, server-side request forgery, or content-security checks that trust the application's own origin as a starting point.

### Examples

=== "Python (Django)"
  ```python
  from urllib import parse
  from django.http import HttpResponseRedirect


  def _extract_redirect(request):
      # Attacker-controlled RelayState / redirect parameter, parsed but never validated.
      raw = request.POST.get("RelayState", "")
      query = parse.parse_qs(parse.urlparse(raw).query)
      redirect_url = (query.get("redirectUrl") or [None])[0]
      return redirect_url


  def login_callback(request):
      redirect_url = _extract_redirect(request) or PORTAL_URL
      # SINK: HttpResponseRedirect writes the Location header verbatim;
      # any https://evil.com value is followed by the victim's browser.
      return HttpResponseRedirect(redirect_url)
  ```

=== "Java (Spring)"
  ```java
  import org.springframework.web.bind.annotation.RequestParam;
  import org.springframework.web.bind.annotation.GetMapping;
  import org.springframework.web.bind.annotation.RestController;
  import org.springframework.web.servlet.view.RedirectView;

  @RestController
  public class LoginController {

      @GetMapping("/login/callback")
      public RedirectView callback(@RequestParam String redirectUrl) {
          // redirectUrl is taken verbatim from the request and never validated.
          return new RedirectView(redirectUrl);
      }
  }
  ```

=== "JavaScript (Express)"
  ```javascript
  const express = require('express');
  const app = express();

  app.get('/login/callback', (req, res) => {
    const redirectUrl = req.query.redirectUrl || '/dashboard';
    // No host/scheme validation: an attacker-supplied https://evil.com is followed.
    res.redirect(redirectUrl);
  });

  app.listen(3000, () => console.log('Server started on port 3000'));
  ```

=== "PHP"
  ```php
  <?php
  // redirectUrl is taken from the request and emitted verbatim in the Location header.
  $redirectUrl = $_GET['redirectUrl'] ?? '/dashboard';
  header('Location: ' . $redirectUrl);
  exit;
  ?>
  ```
