Mobile Applications must use Transport Layer Security (TLS) to provide encryption at the transport layer and ensure the confidentiality and integrity of data in transit.This application does not use SSL/TLS and is vulnerable to traffic interception and modification.

An attacker performing a man-in-the-middle (MITM) attack may:

*   Passively intercept the communication to access any sensitive data in transit like usernames, passwords or credit card number
*   Actively inject or remove content to forge and omit information or inject malicious scripts
*   Actively redirect the communication to the attacker in the context of the initial trusted party
