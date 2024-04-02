To avoid having credentials leaked in application logs and/or backend servers logs, consider the following:

- Avoid hardcoding credentials and/or session tokens in URL
- Use `POST` method instead of `GET` to submit credentials
- Always use SSL to protect request credentials from MiTM attacks.