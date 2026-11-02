GitLab Community Edition (CE) and Enterprise Edition (EE) contain a critical integer overflow vulnerability (CVE-2026-97229, CWE-190, CVSS 10.0 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H`) in the compilation of user-supplied regular expressions from CI/CD configurations. Under certain conditions, an **unauthenticated** user can execute arbitrary code on the GitLab server by supplying a specially crafted regular expression in a CI/CD configuration, because the expression is not validated sufficiently before being compiled.

The root cause is in Ruby's regular expression engine (Onigmo). GitLab compiles regular expressions supplied by its users — such as patterns in CI configuration — with `Regexp.new`. A specially crafted pattern overflows an integer that holds the size of the compiled pattern while Ruby compiles it, corrupting memory in a way that can be turned into remote code execution. The underlying Ruby bug is fixed by ruby/ruby pull request #19020. GitLab addressed the issue in its own releases by patching the Ruby it ships ("Add Ruby regexp program size patch for 3.3 and 3.4"); Ruby fixed it upstream in Ruby 3.4.12, 3.3.13 and in the 4.0 series (4.0.8, with follow-up fixes in 4.0.9).

GitLab assigned four CVEs to bugs in this class, all found through GitLab's bug bounty program; a finding on a self-managed GitLab instance may cite any of them:

* **CVE-2026-97229** — integer overflow in the **CI/CD** regular expression compiler, fixed in GitLab **19.4.2** (also fixed in 19.3.5 and 19.2.8).
* CVE-2026-89078 — double free in the regular expression parser, fixed in GitLab 19.4.1.
* CVE-2026-93577 — integer overflow in the regular expression compiler, fixed in GitLab 19.4.1.
* CVE-2026-110264 — overflow of internal IDs in a pattern with many repeats, fixed in GitLab 19.5.1.

### Affected versions

* GitLab CE/EE 19.2 before 19.2.8
* GitLab CE/EE 19.3 before 19.3.5
* GitLab CE/EE 19.4 before 19.4.2

GitLab.com and GitLab Dedicated were patched before the public release; self-managed installations are affected. The vulnerability was added to the CISA Known Exploited Vulnerabilities catalog on October 29, 2026.

### How the weakness generalizes

The reachability condition is not GitLab-specific: any application that **compiles a regular expression from a string an attacker controls** — passing it to `Regexp.new`, `Regexp.union` or `Regexp.compile`, or interpolating it into a regexp literal such as `/#{input}/` — is a potential target for this class of memory-corruption bugs in Onigmo, even if the application is not GitLab. Ruby's guidance is explicit that applications that only use regular expressions written by their own developers are not affected. Note that neither `Regexp.timeout` nor limiting the length of patterns provides reliable protection: a timeout does not guard against corruption that happens during compilation, and some of the bugs in this class can be triggered by short patterns.

=== "Ruby"
  ```ruby
    # Vulnerable: compiles a regular expression built from untrusted input.
    class Ci::LintController < ApplicationController
      def create
        pattern = params[:rules_pattern]   # attacker-controlled
        regexp  = Regexp.new(pattern)       # integer overflow during compilation -> RCE
        Config::Validator.new(regexp).run
      end
    end

    # Fixed behavior: GitLab 19.4.2 patches the bundled Ruby (Onigmo) so that
    # compiling such a pattern no longer overflows. Applications that are not
    # GitLab should avoid compiling regexps from untrusted input altogether.
  ```

=== "Bash"
  ```bash
    # Identify the version of a self-managed GitLab instance.
    # The help page footer shows the version (sign in may be required):
    curl -sk "https://gitlab.example.com/help" | grep -oE \
      "GitLab (Community|Enterprise) Edition [0-9]+\\.[0-9]+\\.[0-9]+"

    # The authenticated REST API also reports it:
    curl -sk -H "PRIVATE-TOKEN: <token>" "https://gitlab.example.com/api/v4/version"
    # {"major":19,"minor":4,"patch":1,"revision":"..."}
    # 19.4.1 < 19.4.2  ->  affected by CVE-2026-97229
  ```

### Validating a finding

* A finding on an instance whose version falls in the ranges above should be treated as a confirmed exposure: exploitation is unauthenticated, remote code execution, and the vulnerability is known to be exploited in the wild. Version identification — from the help page footer, the `api/v4/version` endpoint, or the instance's inventory record — is the practical evidence; the exploit itself must not be run against a production instance.
* Benign lookalikes: a GitLab instance at 19.2.8+, 19.3.5+, 19.4.2+ or 19.5+ is not affected by this specific CVE (check the sibling CVEs above for their own boundaries), and GitLab.com/GitLab Dedicated tenants were patched by the vendor. A version string obtained from a proxy, a cached page, or a different virtual host than the one scanned is not valid evidence — confirm the version against the exact scanned host.

### Detecting exploitation attempts

GitLab published six threat detections for self-managed instances: `Onigmo native worker crash`, `Graphql cilint hostile regexp`, `ci regexp oversized non ascii path`, `ci regexp guard rejection`, `ci lint workhorse worker crash` and `ci lint scripted client error burst`. Repeated crashes of the CI lint workers or regexp guard rejections in a short window on an unpatched instance are strong indicators of probing or exploitation.
