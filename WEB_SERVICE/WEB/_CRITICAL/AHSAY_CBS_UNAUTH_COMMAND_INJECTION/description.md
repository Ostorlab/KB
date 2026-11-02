AhsayCBS (Ahsay Cloud Backup Suite) is a server-side backup platform whose web console and RESTful API are frequently exposed to the internet by managed-backup providers. Two flaws in the product, tracked as **CVE-2026-105133** and **CVE-2026-105134**, together give a remote, unauthenticated attacker code execution on the server, and CISA added both to the Known Exploited Vulnerabilities catalog on October 14, 2026.

* **CVE-2026-105134** (CWE-77/CWE-78, operating-system command injection) — the flaw is in the Replication Receiver component, reachable through the `/rps/api/json/UpdateReceivers.do` API endpoint. Manipulating the `random` argument to that endpoint injects operating-system commands. The CNA record scores it CVSS 3.1 base **10.0** (`AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H`) and notes the exploit has been published and may be used.
* **CVE-2026-105133** (CWE-287, improper authentication) — the `checkSysPwd` function of `com/ahsay/obs/api/ApiStructsAction.java` (the API component) does not correctly validate the `random` argument, which results in improper authentication and lets a remote attacker bypass the system-password check (CVSS 3.1 base 7.3). This bypass is the natural companion to the command-injection flaw on the same API surface.

A critical detail for triage: **the first patch round did not fully fix either flaw.** Ahsay's October 12, 2026 announcement states that the earlier patches **v9.15.2.59 and v10.3.4.0 did not fully address** the vulnerabilities, and instructs partners to apply a second-round hotfix — **AhsayCBS 9.15.2.70** for the v7, v8 and v9 tracks or **AhsayCBS 10.3.4.45** for the v10 track — and to **reboot the server after applying the hotfix**. Per the CNA records, all builds up to 9.15.2.69 and 10.3.4.44 are affected.

### Affected versions

* **v7, v8 and v9 tracks**: affected up to and including **9.15.2.69** (including every build that carries the first patch, 9.15.2.59 and later). Fixed by the **9.15.2.70** hotfix.
* **v10 track**: affected up to and including **10.3.4.44** (including every build that carries the first patch, 10.3.4.0 and later). Fixed by the **10.3.4.45** hotfix.
* Both hotfixes require a **server reboot** to take effect; a running process that has not been restarted may still be vulnerable.

### Distinguishing a real finding from a benign lookalike

The reportable condition is an AhsayCBS server whose version is **below the second-round hotfix** for its track and whose console/API is reachable — in particular when it is reachable from the internet. A version fingerprint of the server (from the console's self-reported build or its API) is sufficient; comparing it against the fixed builds above decides the finding. Exploitation in the wild is already documented (CISA KEV, both CVEs; Huntress's write-up covers the flaws' exploitation), so an internet-exposed unpatched server should be treated as an exposure finding with high urgency, not as a theoretical issue.

The following signals are **not** evidence of the vulnerability on their own:

* An AhsayCBS login page or product branding — this only fingerprints the product.
* A version between the first patch and the second hotfix *looking* patched (for example a server reporting 9.15.2.59–9.15.2.69 or 10.3.4.0–10.3.4.44). These builds **carry the first, incomplete patch and remain vulnerable** — this is the single most important triage trap for this entry.
* A `403` or bot-challenge response on the console host — an edge-layer mitigation response, not an application authorization decision.

Do not verify this finding by sending crafted `random` payloads against a production backup server: the command-injection payload executes on the target if it is vulnerable. A version fingerprint plus the fixed-build boundary is the safe, sufficient verification.

  ```bash
    # Benign verification (version fingerprint only — do NOT send injection payloads):
    # 1) Fingerprint the AhsayCBS web console / API build of the target server.
    # 2) Compare the reported build against the fixed versions:
    #    - v9 track: fixed in 9.15.2.70 (builds 9.15.2.59 .. 9.15.2.69 are NOT fixed)
    #    - v10 track: fixed in 10.3.4.45 (builds 10.3.4.0 .. 10.3.4.44 are NOT fixed)
    #    - any build below the first patch is equally affected.
    # A reboot after hotfix is required; a server reporting a fixed build that has
    # not been rebooted since applying it may still be running vulnerable code.
  ```

### Detection of exploitation attempts

* Review AhsayCBS server logs and the Replication Receiver configuration for unexpected changes around `/rps/api/json/UpdateReceivers.do`, in particular unexpected receiver entries or argument values, since the command-injection flaw is reached through that endpoint.
* On an internet-exposed server that ran an affected build, assume compromise until investigated, per CISA's KEV required action, which references its forensics triage guidance (BOD 26-04). Backup servers hold both customer backup data and encryption-key material: investigate for credential theft and for tampering with backup sets, and rotate all administrative and stored credentials after rebuilding from a known-good state.
