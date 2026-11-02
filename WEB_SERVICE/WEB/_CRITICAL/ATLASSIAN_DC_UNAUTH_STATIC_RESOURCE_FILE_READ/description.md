Bitbucket Data Center, Confluence Data Center, Jira Software Data Center, Jira Service Management Data Center, Bamboo Data Center, Crowd Data Center, Crucible and Fisheye all contain an unauthenticated arbitrary-file-read weakness in their static-resource download endpoints (CVE-2026-21589, CWE-552; rated Critical 9.3 by Atlassian under CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H, and 7.5 under CVSS:3.1 by NVD). CISA added it to the Known Exploited Vulnerabilities catalog on October 15, 2026.

The affected products serve plugin web resources without authentication through paths such as `/s/<build>/_/download/resources/<plugin-key>:<plugin-resource>` (Jira, Confluence, Bitbucket and the others each expose the same `download/resources` family). The path is resolved using the Atlassian plugin separator `:`, and it does not neutralize traversal segments written with that separator: a remote, unauthenticated attacker can walk out of the resource directory using `..::` segments and read files **within the web application root directory** whose exact name and path are already known. Exploitation does not allow listing or enumerating directory contents — an attacker cannot discover file names through this weakness, only read files they can already name. In some configurations, sensitive files present under the web application root increase the impact.

The public detection script published by watchTowr demonstrates the exact request shapes: for Jira `download/resources/jira.webresources:color-picker-popup/images/..::..::..::..::..::WEB-INF::web.xml`, for Confluence `s/1/_/download/resources/com.atlassian.confluence.plugins.dashboard-actions/images/..::..::..::..::..::..::..::..::WEB-INF::web.xml`, and for Bitbucket `s/1.0/_/download/resources/com.atlassian.bitbucket.server.bitbucket-webpack-INTERNAL:avatar/avatar/..::..::..::..::..::WEB-INF::urlrewrite.xml`.

All versions of the listed Data Center products released before their fix versions are affected — the related vendor tickets (BSERV-20604, CONFSERVER-104488, JRASERVER-79546, JSDSERVER-16809, BAM-26567, CWD-6610, CRUC-8741, FE-7583) indicate the flaw is not tied to a recent regression. Atlassian's cloud products were already patched at disclosure; Atlassian found no evidence of exploitation of the cloud, and no cloud customer action is required.

### Affected and fixed versions

All versions prior to the first fixed release of each product are affected:

| Product | First fixed versions |
| --- | --- |
| Bitbucket Data Center | 9.4.26, 10.2.8, 10.5.1 |
| Confluence Data Center | 9.2.26, 10.2.19 |
| Jira Software Data Center | 9.12.40, 10.3.26, 11.3.12 |
| Jira Service Management Data Center | 5.12.40, 10.3.26, 11.3.12 |
| Bamboo Data Center | 10.2.24, 12.1.12 |
| Crowd Data Center | 6.3.7, 7.0.3, 7.1.7, 7.2.4 |
| Crucible | 4.9.15 |
| Fisheye | 4.9.15 |

### Distinguishing a real finding from a benign lookalike

Concrete evidence of the vulnerability is an unauthenticated request to a `download/resources`-family endpoint whose path contains `..::` (or URL-encoded/double-encoded variants of `..` adjacent to `/`, `\` or `::`) and whose response returns the **content of the targeted file** — for example the `WEB-INF/web.xml` deployment descriptor — rather than an error page.

The following signals are **not** evidence on their own:

* A single `:` in a `download/resources` path (for example `jira.webresources:color-picker-popup`) — the plugin separator is the normal, legitimate syntax of these endpoints; the indicator is the `..::` traversal sequence, not the colon.
* A `404` or error response from a `download/resources` path that carries traversal segments — an error response means the traversal did not resolve to a file, which is not evidence that a different traversal would also fail.
* A login page or product version banner identifying Jira, Confluence or Bitbucket — that is only a product fingerprint; the finding requires the traversal request and the file content in the response.
* Atlassian Cloud (`atlassian.net` domains) — the cloud was already patched and is out of scope of this weakness.

=== "Bash"
  ```bash
    # Benign detection against an authorized instance (reads only the
    # non-sensitive deployment descriptor; do NOT target credential files):
    curl -sk -o /tmp/out.xml -w '%{http_code}\n' \
      "https://jira.example.com/download/resources/jira.webresources:color-picker-popup/images/..::..::..::..::..::WEB-INF::web.xml"

    # A 200 whose body starts with '<?xml' and contains <web-app> confirms the
    # unauthenticated file read. On a fixed version the same request fails.
    head -c 200 /tmp/out.xml
  ```

### Detection of exploitation attempts

Atlassian's recommended log check: URL-decode each access-log request line up to two decoding passes, then look for `..` immediately adjacent to `/`, `\` or `::` — which also catches encoded (`%2e%2e%2f`, `%252e`) forms. Requests to any `/download/resources/` or `/_/download/resources/` endpoint carrying such sequences, and any request whose response size matches a known file in the web application root (for example `WEB-INF/web.xml`), should be treated as exploitation attempts. Because the read requires prior knowledge of the file name, successful retrievals frequently target `WEB-INF/web.xml`, `WEB-INF/urlrewrite.xml` and other deployment descriptors first.
