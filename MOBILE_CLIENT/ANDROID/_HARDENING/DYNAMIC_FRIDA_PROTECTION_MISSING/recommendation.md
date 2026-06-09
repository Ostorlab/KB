Detect Frida's presence at runtime and terminate or degrade when it is found.

**Detection approaches:**

1. **Process map scanning:** Read `/proc/self/maps` and scan for frida-related strings (`frida`, `gum-js-loop`, `frida-agent`).

```java
try (BufferedReader reader = new BufferedReader(new FileReader("/proc/self/maps"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        if (line.contains("frida") || line.contains("gum-js-loop")) {
            throw new SecurityException("Instrumentation framework detected.");
        }
    }
}
```

2. **Port scanning:** Frida's default server port is 27042. Detecting an open local port is a lightweight signal.

3. **Named pipe / D-bus detection:** Check for Frida's IPC artifacts in `/tmp` or via D-bus enumeration.

4. **Native integrity check:** Implement detection in a JNI function to resist easy hook patching from Java.

**Additional hardening:**

- Perform checks in multiple locations and at different lifecycle points (startup, background thread, on sensitive operations).
- Obfuscate check logic and check strings to resist static analysis.
- Combine with root detection — Frida typically requires a rooted or otherwise instrumented device.
- Terminate or wipe sensitive state immediately on detection rather than degrading gracefully.
