The application was installed on a rooted/jailbroken device and continued to run normally, with no detection or restriction in place.

A rooted/jailbroken device removes the platform sandbox: any user — or any malware running with elevated privileges — has unrestricted access to the application's process memory, private storage, and inter-process communication channels. An app that does not detect this condition cannot enforce the OS security boundary it normally relies on, and any sensitive data or business logic shipped inside the app should be considered exposed.

**Common attack scenarios:**

- **Sandbox bypass:** Read the app's private storage and databases directly from a privileged shell, bypassing the per-app isolation the OS would otherwise enforce.
- **Runtime instrumentation:** Attach a dynamic instrumentation framework to hook sensitive methods, dump keys, or alter business logic at runtime.
- **Credential and token theft:** Extract material from platform-backed key storage while it is unlocked, and harvest session tokens from process memory.
- **Combined attack:** Pair elevated device privileges with a re-signed or patched build to disable in-app license checks, anti-cheat, or fraud controls.
