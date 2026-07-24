The application continued to run normally with Frida attached and its hook script injected into the running process.

When Frida is active, an attacker can intercept and modify any Java or native method at runtime — bypassing signature checks, license validation, root detection, certificate pinning, and other security controls without modifying the APK.

**Common attack scenarios:**

- **Anti-tampering bypass:** Hook signature verification or root detection methods to return expected values while the attacker-controlled environment remains in place.
- **Secrets extraction:** Intercept cryptographic operations to extract keys, tokens, or session credentials from memory.
- **Logic manipulation:** Modify return values of business logic methods (e.g., payment validation, access control) in real time.
- **Combined attack:** Use Frida alongside a repackaged APK to bypass both static and runtime protections simultaneously.
