For secure and reliable encryption, it is crucial to use modern and robust cryptographic algorithms that have undergone extensive scrutiny and are widely adopted by the industry. Two recommended alternatives to the insecure DES and Triple DES are the Advanced Encryption Standard (AES) and Elliptic Curve Cryptography (ECC).

AES is widely recognized as a highly efficient and secure symmetric encryption algorithm. It offers key lengths of 128, 192, and 256 bits, making it suitable for various encryption purposes. AES has proven to be resilient against most known attacks, making it an excellent choice for data protection.

ECC, on the other hand, is an asymmetric encryption technique that uses pairs of public and private keys for encryption and decryption. ECC is known for providing strong security with shorter key lengths compared to other asymmetric algorithms like RSA. This results in faster encryption and decryption processes while maintaining a high level of security.

To ensure the utmost security when using any cryptographic algorithm, it is essential to follow best practices:

- Key Length: Use key lengths that are considered secure. For AES, 128 bits are sufficient for most use cases, but you can opt for 192 or 256 bits for more sensitive data.

- Cipher Mode: Always employ secure cipher mode settings, such as AES-GCM (Galois/Counter Mode) or AES-CBC (Cipher Block Chaining) with appropriate padding.

- Key Management: Implement a robust key management system to safeguard encryption keys, ensuring they are not compromised.

- Regular Updates: Stay up-to-date with the latest cryptographic standards and practices to address emerging threats and vulnerabilities.

- Secure Implementation: Pay attention to secure coding practices during algorithm implementation to prevent potential vulnerabilities.

- Secure Transmission: When exchanging encrypted data, ensure secure transmission protocols such as TLS (Transport Layer Security) are used to protect data in transit.

By adhering to these best practices and adopting secure algorithms like AES and ECC, you can significantly enhance the security of your cryptographic operations and safeguard sensitive information from unauthorized access. Avoiding the use of insecure algorithms, such as DES and Triple DES, is crucial to maintaining a strong security posture in today's rapidly evolving threat landscape.

# Code Examples:

### Dart

```dart
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:crypto/crypto.dart';
import 'package:pointycastle/export.dart' as pc;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Secure Encryption Demo'),
        ),
        body: EncryptionWidget(),
      ),
    );
  }
}

class EncryptionWidget extends StatefulWidget {
  @override
  _EncryptionWidgetState createState() => _EncryptionWidgetState();
}

class _EncryptionWidgetState extends State<EncryptionWidget> {
  final _controller = TextEditingController();
  String _encryptedText = '';

  void _encryptText() {
    final key = utf8.encode('securekey123456789012345678901234'); // 32 bytes for AES-256
    final iv = Uint8List(16); // 16 bytes for AES
    final s = pc.SICStreamCipher(pc.AESFastEngine())
      ..init(true, pc.ParametersWithIV(pc.KeyParameter(key), iv));
    final input = utf8.encode(_controller.text);
    final output = s.process(input);
    setState(() {
      _encryptedText = base64.encode(output);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        TextField(
          controller: _controller,
          decoration: InputDecoration(
            labelText: 'Enter text to encrypt',
          ),
        ),
        RaisedButton(
          onPressed: _encryptText,
          child: Text('Encrypt'),
        ),
        Text('Encrypted text: $_encryptedText'),
      ],
    );
  }
}
```

### Swift

```swift
import Foundation
import CommonCrypto

func AES_Encrypt(input: String, key: String) -> String {
    let data = input.data(using: String.Encoding.utf8)!
    let keyData = key.data(using: String.Encoding.utf8)!
    let keyBytes = keyData.withUnsafeBytes { (bytes: UnsafePointer<UInt8>) -> UnsafePointer<UInt8> in
        return bytes
    }
    let dataLength = Int(data.count)
    let buffer = UnsafeMutablePointer<UInt8>.allocate(capacity: dataLength + kCCBlockSizeAES128)
    let bufferPtr = UnsafeMutableRawPointer(buffer)
    let bufferPtrBytes = bufferPtr.bindMemory(to: Void.self, capacity: dataLength)
    let iv = [UInt8](repeating: 0, count: kCCBlockSizeAES128)
    var numBytesEncrypted :size_t = 0
    let cryptStatus = CCCrypt(CCOperation(kCCEncrypt), CCAlgorithm(kCCAlgorithmAES), CCOptions(kCCOptionPKCS7Padding), keyBytes, kCCKeySizeAES128, iv, data.bytes, dataLength, bufferPtrBytes, dataLength + kCCBlockSizeAES128, &numBytesEncrypted)
    if UInt32(cryptStatus) == UInt32(kCCSuccess) {
        let encryptedData = Data(bytes: UnsafePointer<UInt8>(buffer), count: numBytesEncrypted)
        buffer.deallocate()
        return encryptedData.base64EncodedString()
    } else {
        buffer.deallocate()
        return ""
    }
}

func main() {
    print("Enter text to encrypt:")
    let input = readLine() ?? ""
    print("Enter encryption key:")
    let key = readLine() ?? ""
    let encrypted = AES_Encrypt(input: input, key: key)
    print("Encrypted text: \(encrypted)")
}

main()
```

### Kotlin

```kotlin
import javax.crypto.Cipher
import javax.crypto.SecretKey
import javax.crypto.SecretKeyFactory
import javax.crypto.spec.PBEKeySpec
import javax.crypto.spec.SecretKeySpec
import java.util.*
import javax.crypto.spec.IvParameterSpec
import java.security.spec.KeySpec
import javax.crypto.SecretKeyFactory
import javax.crypto.spec.PBEKeySpec
import java.security.SecureRandom

fun main(args: Array<String>) {
    val scanner = Scanner(System.`in`)
    println("Enter text to encrypt:")
    val text = scanner.nextLine()
    println("Enter AES key:")
    val key = scanner.nextLine()

    val salt = ByteArray(16)
    SecureRandom().nextBytes(salt)
    val factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256")
    val spec: KeySpec = PBEKeySpec(key.toCharArray(), salt, 65536, 256)
    val secretKey = factory.generateSecret(spec)
    val secretKeySpec = SecretKeySpec(secretKey.encoded, "AES")

    val encryptedText = encrypt(text, secretKeySpec)
    println("Encrypted text: $encryptedText")

    val decryptedText = decrypt(encryptedText, secretKeySpec)
    println("Decrypted text: $decryptedText")
}

fun encrypt(text: String, key: SecretKey): String {
    val cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
    val iv = ByteArray(16)
    SecureRandom().nextBytes(iv)
    val ivSpec = IvParameterSpec(iv)
    cipher.init(Cipher.ENCRYPT_MODE, key, ivSpec)
    return Base64.getEncoder().encodeToString(cipher.doFinal(text.toByteArray()))
}

fun decrypt(text: String, key: SecretKey): String {
    val cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
    val iv = ByteArray(16)
    SecureRandom().nextBytes(iv)
    val ivSpec = IvParameterSpec(iv)
    cipher.init(Cipher.DECRYPT_MODE, key, ivSpec)
    return String(cipher.doFinal(Base64.getDecoder().decode(text)))
}
```
