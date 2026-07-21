To mitigate the risk of open redirects, validate every redirect destination against an explicit allowlist of hosts and schemes before issuing the redirect response. The recommendations are:

* __Validate the redirect destination with a host allowlist__: before sinking a user-controllable value into a redirect, pass it through the framework's safe-URL helper, e.g. Django's `django.utils.http.url_has_allowed_host_and_scheme(url, allowed_hosts={...}, require_https=True)`. Reject the value (fall back to a safe default) when the check fails.
* __Prefer relative paths__: when the redirect is meant to stay inside the application, only allow relative paths (no scheme, no authority). Reject protocol-relative values such as `//evil.com` explicitly — they are treated as cross-origin navigations by the browser.
* __Do not rely solely on scheme allowlists__: a framework scheme allowlist (e.g. `["http", "https"]`) blocks `javascript:`/`data:` but still permits any external `http`/`https` host, which is exactly this bug. Always pair it with a host allowlist.
* __Do not trust request-derived host values__: never build the redirect destination from the `Host` header, `X-Forwarded-Host`, or `Referer` without an explicit allowlist.
* __Centralize redirect validation__: enforce the allowlist in a single helper used by every redirect site, so the policy cannot be forgotten at a new endpoint. Define an explicit `ALLOWED_REDIRECT_HOSTS` set in the application settings.

### Examples

=== "Python (Django)"
  ```python
  from django.utils.http import url_has_allowed_host_and_scheme
  from django.http import HttpResponseRedirect

  ALLOWED_REDIRECT_HOSTS = {"report.ostorlab.co", "api.ostorlab.co"}


  def _safe_redirect(redirect_url, request):
      if redirect_url and url_has_allowed_host_and_scheme(
          redirect_url,
          allowed_hosts=ALLOWED_REDIRECT_HOSTS,
          require_https=request.is_secure(),
      ):
          return redirect_url
      return None


  def login_callback(request):
      redirect_url = _extract_redirect(request)
      # Reject external/protocol-relative/javascript: values; fall back to a safe default.
      redirect_url = _safe_redirect(redirect_url, request)
      url = redirect_url or PORTAL_URL
      return HttpResponseRedirect(url)
  ```

=== "Java (Spring)"
  ```java
  import java.net.URI;
  import java.util.Set;
  import org.springframework.web.servlet.view.RedirectView;

  @RestController
  public class LoginController {

      private static final Set<String> ALLOWED_HOSTS = Set.of("report.ostorlab.co", "api.ostorlab.co");

      @GetMapping("/login/callback")
      public RedirectView callback(@RequestParam(required = false) String redirectUrl) {
          String safe = sanitize(redirectUrl);
          return new RedirectView(safe);
      }

      private String sanitize(String redirectUrl) {
          if (redirectUrl == null || redirectUrl.isBlank()) {
              return "/dashboard";
          }
          try {
              URI uri = URI.create(redirectUrl);
              String host = uri.getHost();
              // Only allow same-origin relative paths or explicitly allowlisted hosts.
              if (host == null && redirectUrl.startsWith("/")) {
                  return redirectUrl;
              }
              if (host != null && ALLOWED_HOSTS.contains(host.toLowerCase())
                      && "https".equalsIgnoreCase(uri.getScheme())) {
                  return redirectUrl;
              }
          } catch (IllegalArgumentException ignored) {
          }
          return "/dashboard";
      }
  }
  ```

=== "JavaScript (Express)"
  ```javascript
  const express = require('express');
  const app = express();

  const ALLOWED_HOSTS = new Set(['report.ostorlab.co', 'api.ostorlab.co']);

  function safeRedirect(redirectUrl) {
    if (!redirectUrl) return '/dashboard';
    try {
      const url = new URL(redirectUrl, 'https://report.ostorlab.co');
      // Relative paths only, or explicitly allowlisted https hosts.
      if (redirectUrl.startsWith('/') && !redirectUrl.startsWith('//')) {
        return redirectUrl;
      }
      if (url.protocol === 'https:' && ALLOWED_HOSTS.has(url.host)) {
        return redirectUrl;
      }
    } catch (_) {}
    return '/dashboard';
  }

  app.get('/login/callback', (req, res) => {
    res.redirect(safeRedirect(req.query.redirectUrl));
  });

  app.listen(3000, () => console.log('Server started on port 3000'));
  ```

=== "PHP"
  ```php
  <?php
  $ALLOWED_HOSTS = ['report.ostorlab.co', 'api.ostorlab.co'];

  function safe_redirect($redirectUrl) {
      if ($redirectUrl === null || $redirectUrl === '') {
          return '/dashboard';
      }
      // Relative path (but not protocol-relative //).
      if (str_starts_with($redirectUrl, '/') && !str_starts_with($redirectUrl, '//')) {
          return $redirectUrl;
      }
      $host = parse_url($redirectUrl, PHP_URL_HOST);
      $scheme = parse_url($redirectUrl, PHP_URL_SCHEME);
      if ($scheme === 'https' && in_array(strtolower($host), $ALLOWED_HOSTS, true)) {
          return $redirectUrl;
      }
      return '/dashboard';
  }

  header('Location: ' . safe_redirect($_GET['redirectUrl'] ?? null));
  exit;
  ?>
  ```
