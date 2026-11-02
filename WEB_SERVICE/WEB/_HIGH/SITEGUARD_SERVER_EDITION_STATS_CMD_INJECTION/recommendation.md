Update SiteGuard Server Edition to a fixed release, or apply the vendor's patch — and preserve the forensic evidence first.

* **Before any update or patch, download and retain the diagnostic information** from the product's web management console (診断情報 → 診断情報をダウンロード). The vendor states that applying the update or the patch may erase attack traces; responders who patch first lose the record needed to determine whether the host was exploited.
* **Update to the fixed release for the platform:**
  * Apache httpd, Nginx and IIS editions: **Ver8.00 Update 5** or later (excluding FreeBSD).
  * FreeBSD Apache httpd and Nginx editions: **Ver7.00 Update 6** or later.
* **If upgrading is not immediately possible, apply the vendor's patch**, which replaces the files used by statistics processing. The patch is available even for end-of-life versions, so unsupported installations have a remediation path too.
* **Verify the statistics feature setting** during the change window. If statistics are not required on that server, disable them — the vulnerable code is then not exercised. The feature is enabled by default, so absence of a deliberate change is not evidence it is off.
* **Treat a confirmed-vulnerable installation as a compromise question, not only a patch task.** The attack is local, so exploitation implies an attacker already had a foothold on the host: investigate how the initial access happened (typically through the web applications the WAF fronts), check for persistence under the web-server account, and rotate credentials accessible from that host.
* **Contact the vendor's support channel or JPCERT/CC** if exploitation is suspected; the vendor's alert names both as contact routes for this vulnerability.
* **Assess the surrounding estate:** other servers in the organization running SiteGuard Server Edition with statistics enabled and below the fixed versions carry the same escalation risk — enumerate them as part of the same response.
