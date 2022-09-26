In cryptography, a cipher (or cypher) is an algorithm for performing encryption or decryption—a series of well-defined
steps that can be followed as a procedure.

There are typically two families:

* Blocker Cipher: A block cipher breaks down plaintext messages into fixed-size blocks before converting them into
  ciphertext using a key.
* Stream Cipher: A stream cipher, on the other hand, breaks a plaintext message down into single bits, which then are
  converted individually into ciphertext using key bits.

Common cipher algorithms:

* `DES` and `Triple DES`: Triple DES was designed to replace the original Data Encryption Standard (DES) algorithm,
  which hackers eventually learned to defeat with relative ease. At one time, Triple DES was the recommended standard
  and the most widely used symmetric algorithm in the industry. Triple DES uses three individual keys with 56 bits each.
  The total key length adds up to 168 bits, but experts would argue that 112-bits in key strength is more accurate.
  Despite slowly being phased out, Triple DES has, for the most part, been replaced by the Advanced Encryption
  Standard (AES).
* `AES`: The Advanced Encryption Standard (AES) is the algorithm trusted as the standard by the U.S. Government and
  numerous organizations. Although it is highly efficient in 128-bit form, AES also uses keys of 192 and 256 bits for
  heavy-duty encryption purposes. AES is largely considered impervious to all attacks, except for brute force, which
  attempts to decipher messages using all possible combinations in the 128, 192, or 256-bit cipher.
* `RSA`: RSA is a public-key encryption algorithm and the standard for encrypting data sent over the internet. It also
  happens to be one of the methods used in PGP and GPG programs. Unlike Triple DES, RSA is considered an asymmetric
  algorithm due to its use of a pair of keys. You've got your public key to encrypt the message and a private key to
  decrypt it. The result of RSA encryption is a huge batch of mumbo jumbo that takes attackers a lot of time and
  processing power to break.
* `ECC`: Elliptic Curve Cryptography (ECC) is a key-based technique for encrypting data. ECC focuses on pairs of public
  and private keys for decryption and encryption of web traffic. ECC is frequently discussed in the context of the
  Rivest–Shamir–Adleman (RSA) cryptographic algorithm. RSA achieves one-way encryption of things like emails, data, and
  software using prime factorization.

`DES`, `Triple DES` are insecure and must not be used. Other algorithms suffer from some weaknesses caused by insecure
cipher mode settings, key size or special key cases.