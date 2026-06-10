Detect Frida's presence at runtime and terminate or degrade when it is found. Use multiple independent detection methods — signature-based checks alone can be bypassed with custom Frida builds.

**Detection approaches:**

1. **Process map scanning:** Scan `/proc/self/maps` for strings associated with Frida's injected libraries and agent threads.

=== "Kotlin"
    ```kotlin
    private val FRIDA_SIGNATURES = listOf(
        "frida-agent", "frida-gadget", "frida-server", "gum-js-loop", "frida-helper"
    )

    fun isFridaInMaps(): Boolean {
        return try {
            File("/proc/self/maps").readLines().any { line ->
                FRIDA_SIGNATURES.any { sig -> line.contains(sig) }
            }
        } catch (_: IOException) {
            false
        }
    }
    ```

=== "Java"
    ```java
    private static final List<String> FRIDA_SIGNATURES = Arrays.asList(
        "frida-agent", "frida-gadget", "frida-server", "gum-js-loop", "frida-helper"
    );

    public static boolean isFridaInMaps() {
        try (BufferedReader reader = new BufferedReader(new FileReader("/proc/self/maps"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                for (String sig : FRIDA_SIGNATURES) {
                    if (line.contains(sig)) return true;
                }
            }
        } catch (IOException ignored) {
        }
        return false;
    }
    ```

2. **WebSocket handshake detection:** Frida's server responds to a WebSocket upgrade request with a fixed, predictable `Sec-WebSocket-Accept` key regardless of which port it is running on. Scanning all ports and matching this key detects Frida even when the default port 27042 has been changed.

=== "Native (C/JNI)"
    ```c
    static const char *FRIDA_WS_KEY = "tyZql/Y8dNFFyopTrHadWzvbvRs=";

    bool detect_frida_listener() {
        struct sockaddr_in addr = {0};
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

        for (int port = 1; port < 65535; port++) {
            addr.sin_port = htons(port);
            int fd = socket(AF_INET, SOCK_STREAM, 0);
            if (connect(fd, (struct sockaddr *)&addr, sizeof(addr)) == 0) {
                const char *req =
                    "GET /ws HTTP/1.1\r\nUpgrade: websocket\r\n"
                    "Connection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n\r\n";
                write(fd, req, strlen(req));
                char res[1024] = {0};
                if (read(fd, res, sizeof(res) - 1) > 0 && strstr(res, FRIDA_WS_KEY)) {
                    close(fd);
                    return true;
                }
            }
            close(fd);
        }
        return false;
    }
    ```

3. **Named pipe detection:** Frida creates named pipes under `/proc/self/fd` for IPC between the agent and the host. Scanning file descriptors for Frida-related pipe names catches injected gadgets.

=== "Kotlin"
    ```kotlin
    fun isFridaNamedPipePresent(): Boolean {
        return File("/proc/self/fd").listFiles()?.any { fd ->
            try {
                fd.canonicalPath.contains("frida")
            } catch (_: IOException) {
                false
            }
        } ?: false
    }
    ```

=== "Java"
    ```java
    public static boolean isFridaNamedPipePresent() {
        File[] fds = new File("/proc/self/fd").listFiles();
        if (fds == null) return false;
        for (File fd : fds) {
            try {
                if (fd.getCanonicalPath().contains("frida")) return true;
            } catch (IOException ignored) {
            }
        }
        return false;
    }
    ```

4. **Thread name detection:** Frida spawns threads with recognisable names. Scanning `/proc/self/task/<tid>/comm` for known Frida thread names detects an attached agent.

=== "Kotlin"
    ```kotlin
    private val FRIDA_THREAD_NAMES = listOf("gum-js-loop", "frida-server", "gmain", "pool-frida")

    fun isFridaThreadPresent(): Boolean {
        return File("/proc/self/task").listFiles()?.any { tid ->
            val comm = File(tid, "comm").readText().trim()
            FRIDA_THREAD_NAMES.any { name -> comm.contains(name) }
        } ?: false
    }
    ```

5. **File artifact detection:** Check for Frida server binaries commonly dropped to device storage.

=== "Kotlin"
    ```kotlin
    private val FRIDA_ARTIFACTS = listOf(
        "/data/local/tmp/frida-server",
        "/data/local/tmp/re.frida.server",
        "/sdcard/frida-server"
    )

    fun isFridaArtifactPresent(): Boolean = FRIDA_ARTIFACTS.any { File(it).exists() }
    ```

6. **Memory-to-disk comparison (frida-agnostic):** Compare the `.text` section of loaded libraries in memory against their on-disk counterparts. Any hooking framework — not just Frida — that modifies instructions at runtime will cause a mismatch. This approach survives custom Frida builds that remove all string signatures.

    Implement via JNI, comparing `mmap`-loaded disk bytes against the live in-process mapping for `libc.so` and your own native library. See [darvincisec/DetectFrida](https://github.com/darvincisec/DetectFrida) for a reference implementation that handles the PLT/TEXT boundary correctly on Android 10+.

**Additional hardening:**

- Run checks from native code (JNI) — Java-layer checks are trivially patched by hooking the return value.
- Obfuscate detection strings; a string like `"frida-agent"` in plaintext can be patched in the binary with a hex editor.
- Schedule checks on a background thread and re-run them periodically — Frida can be attached after app startup.
- Combine with root detection; Frida server typically requires root or an unlocked bootloader.
- On detection, terminate immediately and wipe any sensitive in-memory state rather than degrading gracefully — graceful degradation is predictable and easier to bypass.
