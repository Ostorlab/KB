Update every Brotli decoder that runs on untrusted input to a fixed version, and update the runtimes that bundle it:

* **C library**: upgrade to **1.0.10** (from any 1.0.x), **1.1.1** (from any 1.1.x) or **1.2.1** (from 1.2.0); anything at or below 1.0.2 predates the vulnerable range.
* **Node.js**: upgrade to **22.23.4 / 24.22.1 / 26.12.1** or later (October 2026 security releases). End-of-life lines receive no fix.
* **.NET**: upgrade to **8.0.33 / 9.0.22 / 10.0.14** or later.
* **Go** (`github.com/andybalholm/brotli`): upgrade to **v1.2.7** or later; **Python**: PyPI `brotli` to **1.2.1**+, `brotlicffi` to **1.2.1.0**+.
* For embedded or vendor-supplied products (Envoy, Istio, proxies, font tooling, data engines, firmware), apply the vendor's fixed release; where none is available yet, remove the product from the untrusted-decompression path.

Prioritize by exposure: **anything that decompresses request bodies or other attacker-controlled Brotli streams first** (APIs and proxies accepting `Content-Encoding: br` request bodies, WOFF2/font processors, archive and data-format tools); the response-encoder side does not need emergency action.

* If the application or API does not need brotli-compressed **request** bodies, disable accepting `Content-Encoding: br` on requests at the frontend — this removes the remotely reachable trigger while updates are scheduled.
* Re-check **secondary embedding**: a patched runtime does not fix a separately bundled native brotli library (server modules, mobile apps, Electron-style packaging) — enumerate those copies independently.
* Treat exposed, previously unpatched decompression services as candidates for compromise review; pair the upgrade with a review of unexpected child processes, crash logs and memory-corruption signals around the decompression endpoints.
