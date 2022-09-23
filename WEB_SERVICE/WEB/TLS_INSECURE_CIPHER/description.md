Transport Layer Security (TLS) starts by the client requesting a secure connection and presenting a list of suppored cipher suites.

Cipher suite is a list of authentication, encryption, message authentication code (MAC) and key exchange algorithms. Each algorithm serve a specific role during the protocol negotiation. Use of a week algorithm might ciriticaly impact the security of the whole channel.

It was identified that the endpoint supports a combination of cipher suites and Secure Sockets Layer / Transport Layer Security (SSL/TLS) protocols that suffer from known cryptographic weaknesses. Therefore they should not be relied upon for effective transport layer security. An attacker with the ability to eavesdrop the connection could influence or even decrypt the traffic that is passing by.

Cryptographic weaknesses have been demonstrated for all the following configurations:

*   Support for deprecated SSL protocol (v2 or v3)
*   Support of cipher suites offering keys smaller than 128bit
*   Support of cipher suites offering `CBC` mode in combination with TLS protocol lower than version 1.1 vulnerable to the BEAST attack
*   Use of compression within TLS vulnerable to the CRIME attack
*   Support of cipher suites offering `RC4` as cipher
*   Support of cipher suites offering `DES` as cipher
*   Support of cipher suites offering `MD5` as signature algorithm
