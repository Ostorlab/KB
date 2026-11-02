Plex Media Server (PMS) is home-media server software whose web service listens on port 32400 and is frequently forwarded directly to the internet so users can stream remotely. Versions before **1.43.3.10861** contain a chain of four weaknesses — named **plex2shell** by the researcher who found them through coordinated disclosure — that together let a remote, unauthenticated attacker execute code with the privileges of the Plex Media Server process. A public proof of concept was released on October 16, 2026, the vendor confirmed on October 19, 2026 that the chain is being **actively and widely exploited** against internet-facing servers (compromised servers have been used to run cryptocurrency miners and proxy software), and CISA added all four CVEs to the Known Exploited Vulnerabilities catalog on October 20, 2026.

Understanding the chain requires the request-trust model PMS uses: requests are classified as **WAN** (internet; almost everything requires a token), **LAN** (local network; extra features), **loopback** (from 127.0.0.1; trusted heavily — the `/system/agents/*` plugin-management API opens with no token at all on loopback) and **owner** (carrying the owner's `local-*` admin token, which grants full server control). The chain abuses every layer of that model:

* **CVE-2026-96652 — unauthenticated SSRF via `/player/timeline`.** The companion-protocol player endpoint gates WAN requests only by checking that an `X-Plex-Token` header *exists* (any junk value passes). The server builds the player-callback URL as `protocol://host:port` from attacker-supplied parameters with no validation, so a full URL placed in the `protocol` parameter makes PMS POST to an address of the attacker's choosing — including its own loopback — from a genuine 127.0.0.1 origin.
* **CVE-2026-96654 — loopback pivot via the agent `searchOne` API.** Because the stage above produced a loopback-origin request, it can reach the token-less `/system/agents/*` plugin API. The identifier guard in `agentservice.py` is wrapped by a `@lock` decorator that discards the early return, so it never stops anything, and the identifier is spliced into an internal loopback URL without encoding; a `?` opens a query string and a `#` truncates the path, letting the attacker forge a call to any plugin function with their own parameters.
* **CVE-2026-96655 — owner-token theft turning into transcoder SSRF.** The plugin framework attaches the owner's admin token (`PLEXTOKEN`) to any outbound request whose URL *starts with* `http://127.0.0.1` — an unbounded prefix match, so `http://127.0.0.1.<attacker>.sslip.io` also qualifies while resolving to the attacker's IP. Forging a call to the bundled TVDB agent's `GetResultFromNetwork` with such a URL exfiltrates the owner admin token to the attacker (the vendor's one-line summary for this CVE is "disclosure of the server owner's admin token"). With owner access, the `/video/:/transcode/universal` endpoint also fetches arbitrary attacker-supplied media URLs — the SSRF the CVE record itself describes, with no host allowlist on the fetch.
* **CVE-2026-96656 — arbitrary file write executed on load.** The `TranscoderH264Options` server preference is appended verbatim to the x264 encoder's option string on every transcode and is writable by the owner. x264's `dump-yuv` debug option writes decoded frames to a caller-chosen path, and with `qp=0` the frames are bit-exact copies of the input — so a carrier video whose frames encode an ELF shared object is written into the Codecs directory. At transcoder startup, Plex's bundled `libavutil` enumerates the Codecs set-directory and `dlopen`s every `.so` file **without** checking for a `lib` prefix, the execute bit, a signature or specific symbols; the ELF constructor runs on load, giving code execution as the Plex service user.

A fifth CVE from the same disclosure shares the affected-version boundary: **CVE-2026-96651**, a path traversal via `/system/agents/media/get` (the `url` parameter is not checked for `../`), which lets an attacker with any valid session token read arbitrary files the target user can access — including the `PlexOnlineToken` — and is also reachable by a LAN-adjacent attacker who controls the client-supplied `X-Forwarded-For` header.

### Affected versions

Per CISA's CSAF record and the NVD descriptions, **all** of CVE-2026-96651, -96652, -96654, -96655 and -96656 affect Plex Media Server **before 1.43.3.10861**; **1.43.3.10861** is the fixed build (the proof of concept demonstrates the chain through 1.43.3.10828). The companion Plex Desktop 1.115.0 release shipped at the same time; the CVE records above apply to the server.

### Distinguishing a real finding from a benign lookalike

The reportable condition is a Plex Media Server whose version is **below 1.43.3.10861** and which is reachable by any potential attacker (directly from the internet, or from the local network). The build version is the deciding signal: it is returned by the server-identity `/identity` endpoint — the object client libraries such as python-plexapi read for exactly this purpose (`Identity.version`) — and by Settings → General in the web client, so a version fingerprint is sufficient to decide the finding. Given the confirmed in-the-wild exploitation, an internet-exposed unpatched server is an urgent finding, not a theoretical one.

Note the severity discrepancy between sources so it does not cause confusion at triage: the per-CVE CNA scores in NVD are low (4.3 for each SSRF, 6.5 for the URL injection, 7.2 for the file write) because each weakness is scored in isolation, and NVD's per-CVE SSVC records (stamped 2026-09-14, before the October 16 PoC) say exploitation: none. The 9.8 rating (`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`) applies to the **chained** primitive, and the vendor's October 19 statement plus the KEV listings are the current exploitation evidence.

The following signals are **not** evidence of the vulnerability on their own:

* Plex branding, the web player UI, or a `401` on protected endpoints — this only fingerprints the product; returning 401 without a valid token is the server behaving correctly.
* Port 32400 being reachable — an exposure finding, and the precondition that makes the chain exploitable, but not itself the vulnerability.
* A version of **1.43.3.10861 or later** — fixed; at most a hardening note to keep automatic updates on.
* NAS package repositories not yet carrying the fix — this delays remediation but does not change the version verdict; the vendor provides manual installation for exactly this case.

=== "Bash"
  ```bash
    # Benign version fingerprint of a Plex Media Server (no payload, no
    # exploitation stages — the PoC writes and executes files and must never
    # be run against a production server):
    curl -s "http://<host>:32400/identity"

    # The response is a MediaContainer XML document whose version attribute
    # carries the server build, e.g. version="1.43.3.10828".
    # version < 1.43.3.10861  -> vulnerable to the plex2shell chain.
    # version >= 1.43.3.10861 -> fixed.
  ```

### Detection of exploitation attempts

* On a server older than 1.43.3.10861 that was reachable from the internet, the vendor's guidance is to **assume it may be compromised**. Compromise indicators published by the vendor: unrecognized processes started by Plex Media Server (named `myawesomeproxy`, `mylovelyminer` or `x12345`), unfamiliar `.so` or `.dll` files in the Plex Codecs folder, outbound connections to `proxystream.st`, and sustained high CPU use while nothing is playing.
* Review `Preferences.xml` for transcoder options the owner did not set — the attacker sets `TranscoderH264Options` to deliver the payload and may leave it behind.
* The public PoC repository ships defender artifacts (`detection/hunt`, `detection/tests`, `detection/yara`) for compromise hunting on the host.
* Rebuild from a clean installation rather than reusing the old data directory when compromise cannot be ruled out, and change the Plex password and sign out all devices after doing so.
