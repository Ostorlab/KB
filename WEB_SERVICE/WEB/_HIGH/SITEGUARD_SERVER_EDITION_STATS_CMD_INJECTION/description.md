SiteGuard Server Edition is a host-based web application firewall from EG Secure Solutions (Japan) that is installed directly into the web server it protects — Apache httpd, Nginx and IIS editions exist, plus FreeBSD variants of the Apache and Nginx editions. Its statistics feature contains an OS command injection (CVE-2026-106931, CWE-78) that the vendor and JPCERT/CC confirm has been **exploited in the wild**. The affected component runs with the web server's elevated privileges, so successful injection executes arbitrary operating-system commands **as root (Unix) or SYSTEM (Windows)** on the server hosting the protected site. CISA added the CVE to the Known Exploited Vulnerabilities catalog on October 20, 2026.

The vendor scores the weakness CVSS:4.0 `AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H` base 8.5 and CVSS:3.0 `AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` base 7.8. Both vectors describe a **local** attack requiring **some privileges on the host**. The realistic shape is privilege escalation on a web server: an attacker who has already gained a limited foothold on the machine (for example through the very web applications the WAF fronts) can use the statistics feature to escalate to root/SYSTEM — the WAF intended to protect the server becomes its escalation path.

### Conditions required

* SiteGuard Server Edition **Ver2.20 or later**, at a version below the fix for the running platform:
  * **Apache httpd, Nginx and IIS editions**: earlier than **Ver8.00 Update 5** (excluding FreeBSD).
  * **FreeBSD Apache httpd and Nginx editions**: earlier than **Ver7.00 Update 6**.
  * Exception: the **IIS edition from Ver3.10 through Ver4.00 Update 4 is not affected**.
* The **statistics feature is enabled** — it is enabled by default, so a default installation that never changed the setting is exposed.

### Distinguishing a real finding from a benign lookalike

The reportable condition is a SiteGuard Server Edition installation whose version is below the fixed release for its platform **and** whose statistics feature is enabled. Both facts are read from the product's own web management console on the affected host; there is no externally observable probe, so a remote scan can only fingerprint the environment, not demonstrate the weakness. The following signals are **not** evidence on their own:

* A Japanese-language site or a SiteGuard-branded support page — at most a hint that the product family may be in use; SiteGuard does not identify itself in the web responses it protects.
* Statistics disabled — the affected code is not exercised; the installation is not exposed.
* An IIS installation between Ver3.10 and Ver4.00 Update 4 — explicitly out of scope per the vendor.
* A version **at or above** Ver8.00 Update 5 (non-FreeBSD) or Ver7.00 Update 6 (FreeBSD) — fixed; at most a patch-management confirmation.

Because the attack is local, also confirm the surrounding compromise question: a finding here usually means a second weakness already let someone onto the host, and the injection turned it into root/SYSTEM.

### Preserving attack traces before remediation

The vendor's alert carries an unusual and important instruction: **download and retain the product's diagnostic information before updating or applying the patch, because the update/patch may erase attack traces**. The diagnostic-information download lives in the web management console (診断情報 → 診断情報をダウンロード). Responders who patch first lose the evidence needed to establish whether the pre-existing foothold was exploited.

The vendor notified customers with direct support contracts on September 29, 2026, published the public alert on October 14, 2026, and coordinates through JPCERT/CC (alert JPCERT-AT-2026-0032; JVN record JVN#88474777).

### Detection of exploitation attempts

* Preserve and review the diagnostic information downloaded before patching — it is the primary artifact for establishing exploitation on the affected host.
* Investigate the host for the earlier compromise that enabled the local attack: web-application-level intrusions on the same server, unexpected local users, and command execution artifacts under the web-server account that precede the statistics-feature activity.
* Coordinate suspected compromise with the vendor's support channel or JPCERT/CC as the alert directs; both are named contact routes in the advisory.
