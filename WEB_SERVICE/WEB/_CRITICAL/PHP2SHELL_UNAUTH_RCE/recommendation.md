Upgrade PHP to the fixed releases **8.2.35, 8.3.36, 8.4.27 or 8.5.12** (or later) immediately — per the vendor advisory, updating is the **only complete mitigation** for both CVE-2026-109618 and CVE-2026-109619. Unsupported lines (PHP 7.x and earlier) have no fixed release; migrate to a supported line.

* **Restart every PHP worker after updating** (FPM pools, Apache children, FrankenPHP processes), and confirm that no pool, directory or application-level setting restores a finite PHP memory limit or an older runtime.
* **For deployments that cannot update immediately**, apply the vendor's interim configuration mitigations, understanding that none of them is complete:
  * set and enforce `memory_limit=-1` administratively — it removes the predictable per-request limit behind the confirmed exploit (it does not stop an OOM when an underlying allocation such as `mmap()` itself fails, and it increases DoS exposure);
  * keep `post_max_size` conservative and enforce the decoded request size independently at the frontend (reverse proxy, WAF);
  * reduce `max_input_nesting_level` and bound the number of input variables, multipart parts, headers within each part and uploads;
  * if the application does not use multipart form data, block such requests at the frontend before they reach PHP;
  * container or cgroup memory limits (`memory.max`) are a partial alternative to PHP's own `memory_limit`, with their own trade-offs; do **not** use `RLIMIT_AS`/`RLIMIT_DATA`, which cause `mmap()` to fail and reproduce the vulnerable condition.
* **Prefer PHP-FPM with a hardened frontend over mod_php.** mod_php invokes the request shutdown procedure unconditionally and applies per-directory INI before request startup, making it the most exposed SAPI for both weaknesses; if FPM is used, do not forward attacker-influenceable `PHP_VALUE`/`PHP_ADMIN_VALUE` parameters from the frontend.
* **Treat affected hosts as potentially compromised.** Both CVEs are exploited in the wild and are chained with Linux kernel CVE-2026-46300 for root-level webshell implantation; pair the upgrade with webshell/IOC triage on any host that was exposed while vulnerable, and patch the kernel side of the chain as well.
* Where the PHP runtime is not directly patchable (appliance or vendor software), request a fixed build from the vendor and apply the frontend mitigations above in the meantime.
