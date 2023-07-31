The use of insecure encryption algorithms such as Data Encryption Standard (DES) and Triple DES (3DES) presents a significant vulnerability in data security. These outdated algorithms have known weaknesses that can be exploited by cybercriminals to decrypt sensitive information. DES, for instance, uses a 56-bit key which is considered relatively easy to crack with modern computing power. Similarly, 3DES, while offering more security than DES by applying the algorithm thrice to each data block, is still vulnerable to certain types of attacks, such as meet-in-the-middle attacks and sweet32 attacks. This vulnerability can lead to unauthorized access to confidential data, potentially resulting in data breaches and other serious security incidents.

### Examples

#### Dart

```dart
dart
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
          title: Text('Insecure Encryption Demo'),
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
    final key = utf8.encode('insecurekey');
    final iv = Uint8List(8);
    final s = pc.SICStreamCipher(pc.DESEngine())
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

#### Swift

```swift
swift
import Foundation
import CommonCrypto

func DES_Encrypt(input: String, key: String) -> String {
    let data = input.data(using: String.Encoding.utf8)!
    let keyData = key.data(using: String.Encoding.utf8)!
    let keyBytes = keyData.withUnsafeBytes { (bytes: UnsafePointer<UInt8>) -> UnsafePointer<UInt8> in
        return bytes
    }
    let dataLength = Int(data.count)
    let buffer = UnsafeMutablePointer<UInt8>.allocate(capacity: dataLength + kCCBlockSizeDES)
    let bufferPtr = UnsafeMutableRawPointer(buffer)
    let bufferPtrBytes = bufferPtr.bindMemory(to: Void.self, capacity: dataLength)
    let iv = [UInt8](repeating: 0, count: kCCBlockSizeDES)
    var numBytesEncrypted :size_t = 0
    let cryptStatus = CCCrypt(CCOperation(kCCEncrypt), CCAlgorithm(kCCAlgorithmDES), CCOptions(kCCOptionPKCS7Padding), keyBytes, kCCKeySizeDES, iv, data.bytes, dataLength, bufferPtrBytes, dataLength + kCCBlockSizeDES, &numBytesEncrypted)
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
    let encrypted = DES_Encrypt(input: input, key: key)
    print("Encrypted text: \(encrypted)")
}

main()
```

#### Kotlin

```kotlin
kotlin
import javax.crypto.Cipher
import javax.crypto.SecretKey
import javax.crypto.SecretKeyFactory
import javax.crypto.spec.DESKeySpec
import java.util.*

fun main(args: Array<String>) {
    val scanner = Scanner(System.`in`)
    println("Enter text to encrypt:")
    val text = scanner.nextLine()
    println("Enter DES key:")
    val key = scanner.nextLine()

    val encryptedText = encrypt(text, key)
    println("Encrypted text: $encryptedText")

    val decryptedText = decrypt(encryptedText, key)
    println("Decrypted text: $decryptedText")
}

fun encrypt(text: String, key: String): String {
    val desKey = SecretKeyFactory.getInstance("DES").generateSecret(DESKeySpec(key.toByteArray()))
    val cipher = Cipher.getInstance("DES")
    cipher.init(Cipher.ENCRYPT_MODE, desKey)
    return Base64.getEncoder().encodeToString(cipher.doFinal(text.toByteArray()))
}

fun decrypt(text: String, key: String): String {
    val desKey = SecretKeyFactory.getInstance("DES").generateSecret(DESKeySpec(key.toByteArray()))
    val cipher = Cipher.getInstance("DES")
    cipher.init(Cipher.DECRYPT_MODE, desKey)
    return String(cipher.doFinal(Base64.getDecoder().decode(text)))
}
```
