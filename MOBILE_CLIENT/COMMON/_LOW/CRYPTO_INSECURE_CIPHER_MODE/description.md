A block cipher processes the data blocks of fixed size. Usually, the size of a message is larger than the block size. Hence, the long message is divided into a series of sequential message blocks, and the cipher operates on these blocks one at a time.

Common block ciphers are:

* `ECB`: (Electronic Code Book) is the most straightforward way of processing a series of sequentially listed message blocks. The user takes the first block of plaintext and encrypts it with the key to produce the first block of ciphertext. He then takes the second block of plaintext and follows the same process with same key and so on so forth. This mode is **insecure and must not be used**.
* `CBC`: (Cipher Block Chaining) provides message dependence for generating ciphertext and makes the system non-deterministic. In CBC mode, the current plaintext block is added to the previous ciphertext block, and then the result is encrypted with the key. Decryption is thus the reverse process, which involves decrypting the current ciphertext and then adding the previous ciphertext block to the result.
* `CFB`: (Cipher Feedback) each ciphertext block gets ‘fed back’ into the encryption process in order to encrypt the next plaintext block. The CFB mode requires an initialization vector (IV) as the initial random n-bit input block. The IV need not be secret. CFB mode differs significantly from ECB mode, the ciphertext corresponding to a given plaintext block depends not just on that plaintext block and the key, but also on the previous ciphertext block. In other words, the ciphertext block is dependent of message.
* `OFB`: (Output Feedback) involves feeding the successive output blocks from the underlying block cipher back to it. These feedback blocks provide string of bits to feed the encryption algorithm which act as the key-stream generator as in case of CFB mode.The key stream generated is XOR-ed with the plaintext blocks. The OFB mode requires an IV as the  initial random n-bit input block. The IV need not be secret.
* `CTR`: (Counter) It can be considered as a counter-based version of CFB mode without the feedback. In this mode, both the sender and receiver need to access to a reliable counter, which computes a new shared value each time a ciphertext block is exchanged. This shared counter is not necessarily a secret value, but challenge is that both sides must keep the counter synchronized.

Most implementation will default to using the insecure `ECB` mode if it is not explicitly specified. The mode of operation used to encrypt the data is vulnerable and should be replaced with a secure one.