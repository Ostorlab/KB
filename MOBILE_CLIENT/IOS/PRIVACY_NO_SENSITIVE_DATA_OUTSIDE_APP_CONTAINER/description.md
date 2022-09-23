To ensure the proper storage of sensitive data, like user credentials, session tokens, PII, sensitive data must not
be stored outside the application container or the system credential storage.

Sensitive data can be exposed through insecure IPC mechanisms or unintentionally leaked to cloud storage, backups or
keyboard cache. The risk of losing the mobile device or have it stolen must therefore account for physical access
scenarios.