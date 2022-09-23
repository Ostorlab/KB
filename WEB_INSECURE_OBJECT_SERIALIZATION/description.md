The application uses an insecure deserialization scheme from untrusted data.

Insecure object deserialization may result in

*   Arbitrary remote code execution
*   Modification of the application logic
*   Data tampering, such as bypassing access control

Exploitation of deserialization vulnerabilties is difficult, due to the absence of off the shelf exploits and the need to to tweak them for the targetted exploit.