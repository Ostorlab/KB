Dynamicaly loading libraries if not handled properly gives room for a range of potential vulnerabilities including:

* **`Insecure Loading Path`**  : occurs when the application loads from an untrusted location or is manipulated to do so, An untrusted location could be hosting malicious libraries.
* **`Library Hijacking`** : involves replacing the legitimate Library with a malicious one.

These vulnerabilities have the potential to allow code injection and execution, privilege escalation and unauthorized access to sensitive resources.