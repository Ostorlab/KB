Check the `FLAG_DEBUGGABLE` flag at runtime and terminate if it is set in a production build.

```java
if ((getApplicationInfo().flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0) {
    throw new SecurityException("Debuggable build detected — terminating.");
}
```

Additional hardening recommendations:

- Perform the check in a native (JNI) function and in multiple locations to resist patching.
- Combine with an `android:debuggable="false"` build configuration enforced by CI to prevent accidental release of debuggable builds.
- Terminate or wipe sensitive state immediately — do not degrade gracefully.
