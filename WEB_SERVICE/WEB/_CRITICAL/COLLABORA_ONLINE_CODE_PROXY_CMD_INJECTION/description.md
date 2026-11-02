The **Collabora Online – Built-in CODE Server** app for Nextcloud (package `richdocumentscode`) contains an unauthenticated operating-system command injection in its `proxy.php` script (CVE-2026-110447, CWE-78; rated Critical 9.2 by MITRE under CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H, and 9.8 under CVSS:3.1 by NVD). A crafted request to the proxy can cause an operating-system command to run as the **web server user**. CISA added it to the Known Exploited Vulnerabilities catalog on October 23, 2026, and it was exploited in the wild in September and October 2026 — Nextcloud operators published real attack logs in the upstream issue tracker.

Two scoping facts decide whether an installation is affected:

* The weakness exists only in the **built-in** CODE Server app (the `richdocumentscode` Nextcloud app). **Standalone Collabora Online servers are not affected.**
* The attack only works **while the built-in CODE server is not running** — i.e. during the window after a container restart, during an upgrade, or after a crash. This is why the CVSS vector carries `AT:P` (attack requirements present): the flaw is dormant while the CODE server process is up, and reappears whenever it is down. Because that state recurs routinely, disabling the app is **not** a workaround — the app must be upgraded to 26.4.303 or later, or removed.

This is **not** the same code path as CVE-2025-66208; the fix for that earlier issue does not prevent this one.

In the wild, exploitation was observed as GET requests to `/apps/richdocumentscode/proxy.php?status` whose path prefix contained a shell command-substitution payload embedded before a traversal — e.g. `GET /x$(<payload>|base64 -d|sh)x/../apps/richdocumentscode/proxy.php?status`, with the `..` traversal URL-encoded (`%2e%2e`) in some samples. The payloads base64-decoded to commands that wrote PHP webshells (for example `shrf4645.php`) into the Nextcloud directory and called back to a per-instance webhook URL.

### Affected and fixed versions

Affected: every release of `richdocumentscode` before **26.4.303**. Fixed: **26.4.303**. Installations on Nextcloud releases at end of life (29 and earlier) cannot upgrade the app to the fixed version and should upgrade Nextcloud or remove the app — the vendor will not provide a fixed release for EOL Nextcloud lines.

### Distinguishing a real finding from a benign lookalike

Concrete evidence is the combination of a Nextcloud installation running the **richdocumentscode app below 26.4.303** (visible in the Nextcloud apps administration page or the `apps/richdocumentscode/` directory) and the proxy being reachable **while the built-in CODE server is stopped**. The version is the finding for scan purposes: a sub-26.4.303 install is affected whether or not the CODE server happens to be running at scan time, because restarts, upgrades and crashes routinely reopen the window.

The following signals are **not** evidence of this vulnerability on their own:

* A **standalone** Collabora Online server (the `coolwsd`/CODE server deployed separately from Nextcloud, or Collabora Online used through its own integration app pointing at it) — out of scope of this CVE.
* Nextcloud with Collabora integration that does **not** use the built-in CODE Server app (for example the `richdocuments` app configured against an external CODE server) — the vulnerable `proxy.php` belongs to the built-in app only.
* `proxy.php` requests in the logs while the CODE server is running normally — normal operation of the app.
* A fixed installation (26.4.303 or later) — patched, regardless of restart state.

=== "Text"
  ```
    # Benign version check in the Nextcloud apps administration page:
    Apps > Your apps > Collabora Online - Built-in CODE Server
    # Version below 26.4.303 -> affected (upgrade to 26.4.303 or remove).
    # Alternatively inspect the app directory (no request is sent):
    ls apps/richdocumentscode/ && grep -m1 '"version"' apps/richdocumentscode/appinfo/info.xml
  ```

Active verification by sending a command-substitution payload to `proxy.php` should not be performed against production systems: a successful payload executes a command as the web server user and leaves attacker-controlled files.

### Detection of exploitation attempts

* Search web-server access logs for requests to `/apps/richdocumentscode/proxy.php` (any `?status` variant) whose request path contains `$(...)` or backtick command-substitution syntax, an unexpected literal prefix before a `..` or `%2e%2e` traversal, or both — that is the observed exploit shape.
* Look for unexpected `.php` files created in the Nextcloud directory (the web server user writing new PHP files is a webshell signature), and for outbound callbacks from the web server to per-instance unique-ID webhook URLs.
* Requests in the logs during upgrade windows or immediately after restarts deserve extra weight — the vulnerability is only reachable while the CODE server process is down, which is exactly when upgrades and restarts happen.
