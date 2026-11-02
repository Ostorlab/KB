PHP 8.2.34 and earlier on the 8.2 line, 8.3.35 and earlier, 8.4.26 and earlier, and 8.5.11 and earlier contain two related memory-corruption weaknesses that a remote, unauthenticated attacker can trigger and combine into remote code execution (RCE). Both were fixed in the same coordinated release — PHP 8.2.35, 8.3.36, 8.4.27 and 8.5.12, released October 22, 2026, the day after CISA's October 21 alert requiring immediate patching — and both are being exploited in the wild under the name PHP2Shell. CISA added both CVEs to the Known Exploited Vulnerabilities catalog on October 26, 2026.

### What are the two weaknesses?

**CVE-2026-109618 — RCE via out-of-memory (OOM) corruption (CVSS 9.8, CWE-416/755).** PHP handles out-of-memory errors by calling `longjmp()` to exit the current context and abort handling of the request. In some contexts, request memory is temporarily reachable before it is fully initialized. If any allocation fails at that point, PHP does not account for the early exit and leaves the request memory in an invalid state. The failed allocation does not need to be related to the invalid memory. The request shutdown procedure may then read or branch on it, and multiple OOM strategies can consistently reach this condition and lead to RCE. OOM is reachable within apparent request limits through, among others:

* a multipart request without a usable declared content length (passes the initial `post_max_size` check and keeps supplying decoded body data),
* a multipart part with an unrestricted number of headers (representing headers inside PHP can use substantially more memory than their wire representation),
* empty file controls (they do not count towards `max_file_uploads` but still create file metadata arrays),
* nested field names multiplying the generated array work, and
* application-specific allocations driven by attacker-controlled input.

**CVE-2026-109619 — RCE via stale global state (CVSS 8.1, CWE-416).** PHP workers retain various global state — error, session, object and extension state — that can point to memory owned by a single request. Some input, configuration, session and error-handling operations run *before* the normal initialization of the next request. They can inadvertently access state that the previous request never reset, causing a use-after-free; a strategically crafted heap layout can produce full RCE. Exploitation needs a **producer** — an operation that stores request-owned state where a later request can reach it — and a **consumer** in a *subsequent* request handled by the *same worker*. Producers include a fatal error, a `require` failure, a parse or compile failure, `Maximum execution time exceeded`, an OOM, or even a nonfatal diagnostic during a late shutdown stage. Two confirmed consumer paths run before normal request initialization:

* **INI diagnostics** — a warning, notice or deprecation raised while applying invalid or deprecated INI settings consumes stale error state. It does not need to be fatal, displayed or logged; changing `error_reporting`, using `@`, or disabling `display_errors`/`log_errors` does **not** protect against this.
* **Session upload progress** — session upload progress handling can consume session or decoder state left by an interrupted request, independent of the INI path.

### Server-API (SAPI) susceptibility

The vendor advisory distinguishes how deployments are exposed, which matters both for triage and for choosing a deployment model during remediation:

* **Apache mod_php** — invokes the request shutdown procedure unconditionally, even when request startup has failed, and applies `.htaccess` / `php_value` / `php_flag` / `php_admin_*` directory configuration before `php_request_startup()`. This makes it susceptible to application-independent attacks, before any application code runs. The most exposed configuration.
* **FrankenPHP** — calls the request shutdown procedure analogously to mod_php; likely susceptible to application-independent attacks.
* **PHP-FPM** — exits the child when request startup fails, which prevents consumption of the invalid state for that path; however FPM is conditionally exposed through the second weakness when a frontend (nginx, Apache `mod_proxy_fcgi`, or another FastCGI client) sends `PHP_VALUE` / `PHP_ADMIN_VALUE` parameters that produce a diagnostic before request initialization, and source analysis supports FPM as susceptible to CVE-2026-109618 after normal startup even without a complete public FPM exploit being demonstrated.
* **LSAPI** — models FPM; application-specific exploits are likely but unvalidated.

### Exploitation context

CISA's alert of October 21, 2026 and the KEV entries record active exploitation of both CVEs across a broad set of industries, with follow-on activity including webshells, credential access, remote-access tooling and ransomware operations. The KEV entries also record that these PHP flaws are chained with **Linux kernel CVE-2026-46300** (a page-cache corruption bug in ESP input processing) to implant PHP webshells and run commands as **root** — see the companion entry for that weakness. Any host found running an affected PHP version should therefore be treated as potentially compromised, not merely as needing a patch.

### Distinguishing a real finding from a benign lookalike

* Concrete evidence for a version-based finding is a **disclosed PHP version in the affected ranges** (below 8.2.35 on the 8.2 line, 8.3.36 on 8.3, 8.4.27 on 8.4, 8.5.12 on 8.5, or any older unsupported line such as PHP 7.x or 5.x), typically from the `X-Powered-By` header, a `PHP/x.y.z` token in the `Server` header, error pages, or phpinfo-style disclosures.
* A version disclosure that is **at or above** the fixed versions is a hardening finding (version disclosure), not this vulnerability.
* **Absence of a PHP version banner is not evidence of safety** — it only means the fingerprint was not obtainable; do not close such a case as "not vulnerable" without another way to establish the runtime version.
* The SAPI determines exploitability confidence: the same affected version behind mod_php is materially more exposed than the same version behind FPM without INI-forwarding frontends. The version finding stands either way; SAPI context belongs in the risk narrative, not in the yes/no decision.

  ```bash
    # Benign version fingerprint checks (no memory-corruption payloads):
    curl -sk -D - -o /dev/null https://example.com/ | grep -iE "x-powered-by|server"
    # A response header such as X-Powered-By: PHP/8.3.35 places the host in the
    # affected range; PHP/8.3.36 or newer is patched for both CVEs.
  ```
