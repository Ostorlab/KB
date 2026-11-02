Ivanti Connect Secure (ICS) VPN appliances contain an authentication bypass vulnerability in how the appliance routes requests between its front-end and back-end processes (CVE-2026-104935, CWE-290). The URL path is used to decide whether a request is allowed, while the `X-DSCGI-PATH` request header determines the CGI script that actually handles it. By sending a request to the unauthenticated `/dana-na/auth/url_default/welcome.cgi` endpoint with an `X-DSCGI-PATH` header pointing to a protected CGI script such as `/home/webserver/htdocs/dana/fb/smb/wu.cgi`, a remote unauthenticated attacker can reach authenticated endpoints. This weakness was exploited in the wild as part of a chain that achieves unauthenticated root-level code execution, tracked across three CVEs:

* **CVE-2026-104935** (fixed October 13, 2026) — the authentication bypass in the CGI request routing combined with a remote code execution primitive in the `wu.cgi` upload handler. `wu.cgi` writes uploaded content to `/home/runtime/tmp/<MD5(filename)>` *before* validating that the upload is a valid ZIP archive; when the validation fails the file is deleted, but for a short window it exists on disk. The attacker uploads a Perl script with a `.zip` extension and then sends parallel requests carrying `X-DSCGI-PATH: /home/runtime/tmp/<MD5(filename)>` to execute the uploaded script before deletion, winning a race between execution and removal.
* **CVE-2026-118527** (CWE-340, predictable numbers or identifiers) — the upload target location is predictable (an unsalted MD5 hash of the attacker-supplied filename), which is what makes the race above reliable. It allows files with attacker-controlled content to be written to a known location on disk and chains with the other two vulnerabilities.
* **CVE-2026-111357** (fixed October 29, 2026, CWE-306) — a privilege escalation. The `dsinvoked` broker runs maintenance tasks as root and looks up which program each task runs in DSCache, a shared configuration store. The exploit patches the `cgi-server` process's in-memory copy of `/home/lib/libdsplibs.so` to modify DSCache, reconfiguring an existing maintenance task to launch the Perl interpreter instead of its legitimate script; `dsinvoked` then executes the attacker's Perl script as root. The exploit verifies root access by checking that `/etc/shadow` is readable, then restores the DSCache entry and the in-memory library to their pre-exploitation state.

The chain was observed being exploited against a fully patched appliance (22.8R2.4 at the time) by the threat actor UTA0576 (Volexity tracking). Commands and results were passed through the exploit channel's HTTPS requests, with no web shell or backdoor installed on disk, and the actor deleted evidence of exploitation from Ivanti debug logs and Linux audit logs. Post-exploitation activity focused on credential theft and data exfiltration: extracting domain/LDAP credentials, harvesting LAPS passwords and BitLocker recovery keys, Kerberoasting, password spraying, LDAP packet capture, and exfiltrating the appliance configuration.

Because the attacker's commands execute in memory and the library patch is restored after use, Ivanti's on-disk Integrity Checker Tool (ICT) may not detect exploitation of this chain; network and memory forensics are required to confirm a compromise.

### Affected versions

Per CISA's October 30, 2026 update of its alert, the affected versions are Ivanti Connect Secure **25.1.1.2 and prior, 25.1.2.2 and prior, and 22.8R2.5 and prior**. Ivanti Connect Secure 22.8 reaches end of life on January 31, 2027. Fixes for CVE-2026-104935 were released on October 13, 2026, and the fix for CVE-2026-111357 (the privilege escalation) on October 29, 2026. All three components must be patched: an appliance patched only for CVE-2026-104935 still contains the privilege escalation and the predictable upload location.

### Distinguishing a real finding from a benign lookalike

Concrete evidence of the authentication bypass is an unauthenticated request to `welcome.cgi` that carries an `X-DSCGI-PATH` header pointing at a protected CGI script and receives the **authenticated** response of that script (for example, the `wu.cgi` file-upload page containing "upload file" and "Browse buttons"), without any credentials. A public Nuclei template exists that verifies exactly this behavior.

The following signals are **not** evidence of the vulnerability on their own:

* A login page referencing `/dana-na/auth/`, `welcome.cgi`, or "Ivanti Connect Secure"/"Pulse Secure" branding — this only fingerprint the product and its version.
* A `403` on the VPN login page — a CDN bot-mitigation challenge (for example `x-vercel-mitigated: challenge`, `cf-mitigated: challenge`, `Retry-After`) is an edge-layer response, not an appliance authorization decision.
* A generic `X-DSCGI-PATH` header seen in traffic — the header has legitimate uses in appliance routing; the indicator is a **mismatch between the URL path and the `X-DSCGI-PATH` value**, where the header targets a script in a different, authenticated context.

=== "Bash"
  ```bash
    # Benign reproduction of the authentication-bypass evidence (do NOT upload files):
    # 1) Fingerprint the appliance login page.
    curl -sk "https://vpn.example.com/" | grep -o "welcome.cgi"

    # 2) Request the public welcome.cgi while routing the request to the
    #    protected wu.cgi upload handler via the X-DSCGI-PATH header.
    curl -sk -H "X-DSCGI-PATH: /home/webserver/htdocs/dana/fb/smb/wu.cgi" \
      "https://vpn.example.com/dana-na/auth/url_default/welcome.cgi"

    # A 200 response containing the upload page (for example 'upload file' and
    # 'Browse buttons') confirms unauthenticated access to a protected CGI
    # endpoint. Any version before the October 13, 2026 patch is affected.
  ```

### Detection of exploitation attempts

* Monitor for large numbers of requests to `/dana-na/auth/url_default/welcome.cgi`, and specifically for requests whose `X-DSCGI-PATH` value does not match the URL path (for example `X-DSCGI-PATH: /home/webserver/htdocs/dana/fb/smb/wu.cgi` or `X-DSCGI-PATH: /home/runtime/tmp/<MD5(filename)>`).
* Check `/tmp/` on the appliance for post-exploitation artifacts, and `/data/.icscap/` for a hidden directory containing a renamed packet-capture tool and rotating capture files.
* Investigate truncated or selectively edited `/home/runtime/dlogs/debuglog` and `/var/log/audit/audit.log` entries.
* On a compromised appliance, lateral movement originating from the ICS device and unexpected LDAP or Kerberos traffic are high-confidence indicators; conduct network and memory forensics rather than relying on the Integrity Checker Tool.
