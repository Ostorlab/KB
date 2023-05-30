Dynamicaly Linking libraries if not handled properly gives room for a range of potential vulnerabilities including:

**`Insecure DLL loading`**  : occurs when the application loads from an untrusted location, which could be hosting malicious libraries.
**`DLL hijacking`** : involves replacing a legitimate DLL with a malicious one.
**`DLL injection`** : happens when an attacker injects the malicious DLL directly into the allocated memory of the targeted process (application).

These attacks have the potential to allow code execution, privilege escalation and unauthorized access to sensitive resources.