Magento's REST API accepts file uploads as part of **cart item custom options** (CVE-2026-48356, CVSS 9.3, CWE-434, tracked by Sansec as **PolyShell**). When a product option has type `file`, Magento processes an embedded `file_info` object — base64-encoded file data, a MIME type and a filename — and writes the file to `pub/media/custom_options/quote/` on the server. Three critical checks are missing from that path:

* **no option ID validation** — the submitted option ID is never verified against the product's actual options;
* **no option type gating** — the file-upload logic triggers regardless of whether the product actually has a file-type option;
* **no file extension restriction** — extensions such as `.php`, `.phtml` and `.phar` are not blocked.

The only validation is an image header check (`getimagesizefromstring`), which a polyglot file — a valid GIF or PNG image that also contains executable PHP — trivially bypasses. The most dangerous endpoints are the **anonymous guest cart routes**, which makes this exploitable without any credentials:

```
POST /V1/guest-carts/:cartId/items            (no authentication)
PUT  /V1/guest-carts/:cartId/items/:itemId   (no authentication)
```

GraphQL mutations use a different code path and are **not** vulnerable.

### Impact by web-server configuration

* **Stored XSS** — all versions before 2.3.5, and any version with a custom web-server configuration that serves the upload directory as active content.
* **RCE via PHP upload** — stock nginx 2.0.0–2.2.x (via the `index.php` filename), any version with a non-stock nginx configuration that passes all `.php` requests to fastcgi, and Apache before 2.3.5 without `php_flag engine 0` in the upload directory.

Even when execution is blocked, the uploaded file **stays on disk**: a later configuration change, server migration or web-server swap can make it executable.

### Affected and fixed versions

The vulnerable code has existed **since the first Magento 2 release**. All Magento Open Source and Adobe Commerce versions up to **2.4.9-alpha2** are affected. The fix timeline: Magento/Adobe Commerce **2.4.9 final (released May 12, 2026)** was the first release containing it, and on **July 14, 2026 Adobe backported the fix to the supported release lines via APSB26-73** — that bulletin is the authoritative per-line fixed-version list, and the NVD record enumerates the affected set as Adobe Commerce 2.4.4–2.4.9, Commerce B2B 1.3.3–1.5.3, and Adobe I/O Events for Commerce 1.6.0–1.21.0. Stores on unsupported or end-of-life lines that never received the backport remain vulnerable until they upgrade.

### Exploitation in the wild (CISA KEV, added 2026-10-27)

Sansec observed probing from March 16, 2026, automated mass scanning from March 19, and attacks against 79.5% of the protected Magento stores it tracks; one wave compromised **471 stores in a single hour**. The chain observed in production: upload a PHP webshell via PolyShell → the webshell drops `accesson.php` backdoors across directories → obfuscated JavaScript loaders are injected into CMS pages and the `cms_block` table (localStorage-persisted skimmer loaders, fingerprinting automated scanners, Keitaro-based traffic distribution, and misspelled crypto-brand phishing domains such as `leqdger.click`). CISA's KEV record lists the Polyshell and Gsocket malware families and Sessionreaper tooling, with the retail industry as the primary target.

### Distinguishing a real finding from a benign lookalike

* Concrete evidence for a **detection** finding is a store version below 2.4.9 — typically fingerprinted benignly via the `Magento_Version` module (`GET /magento_version`, which discloses e.g. `Magento/2.4.7 (Community)`), or confirmed from the admin panel / `composer.lock` in a source-code scan.
* **Do not verify this vulnerability by uploading a file.** An upload probe is not a benign check: even when web access to the upload directory is blocked, the file lands on disk (Sansec explicitly notes that only a WAF rule blocking the API call itself stops the upload; blocking the upload directory does not). Version evidence plus configuration review is the correct, non-intrusive confirmation.
* Absence of the `/magento_version` endpoint means the fingerprint could not be obtained — **not** that the store is patched or absent.
* A guest cart endpoint responding `404`/`400` to malformed items is not evidence of safety: the vulnerable parameter is the embedded `file_info` inside an otherwise valid request, not the route's existence.
* The **GraphQL** mutation path is not vulnerable — a finding based only on GraphQL reachability is not this CVE.

  ```bash
    # Benign version fingerprint (no uploads are performed):
    curl -s https://store.example.com/magento_version
    # A result such as "Magento/2.4.7 (Community)" places the store in the
    # affected set; 2.4.9 final or later contains the fix.
  ```

### Detection of exploitation

* Inspect `pub/media/custom_options/` (especially `quote/`) for unexpected files, polyglot images containing PHP, and `index.php` drops.
* Search for `accesson.php` backdoors across directories, and for obfuscated loaders in CMS pages and the `cms_block` database table.
* Review published indicators of compromise from the linked Sansec research (loader domains, localStorage keys, beacon values) and scan for them; a store that ever loaded one of the loader domains should be treated as attacker-writable at the database level — removing the injected script does not remove that access.
