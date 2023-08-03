
# Class Loading Hijacking

Android Class Loading Hijacking is a security vulnerability that allows an attacker to execute malicious code on an Android device by exploiting the way Android loads classes. This is achieved by tricking the Android system into loading a malicious class instead of the intended one. The attacker can then use this malicious class to gain unauthorized access to sensitive data, manipulate the device's functionality, or even take full control of the device. This vulnerability is particularly dangerous because it can be exploited without the user's knowledge, and it can affect any app that does not properly secure its class loading process.

### Examples

#### Dart

```dart
dart
import 'package:flutter/material.dart';
import 'dart:core';
import 'dart:mirrors';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Vulnerable Flutter App'),
        ),
        body: Center(
          child: MyCustomForm(),
        ),
      ),
    );
  }
}

class MyCustomForm extends StatefulWidget {
  @override
  MyCustomFormState createState() {
    return MyCustomFormState();
  }
}

class MyCustomFormState extends State<MyCustomForm> {
  final _formKey = GlobalKey<FormState>();
  final myController = TextEditingController();

  @override
  void dispose() {
    myController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          TextFormField(
            controller: myController,
            validator: (value) {
              if (value.isEmpty) {
                return 'Please enter some text';
              }
              return null;
            },
          ),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 16.0),
            child: RaisedButton(
              onPressed: () {
                if (_formKey.currentState.validate()) {
                  Scaffold.of(context)
                      .showSnackBar(SnackBar(content: Text('Processing Data')));
                  loadClass(myController.text);
                }
              },
              child: Text('Submit'),
            ),
          ),
        ],
      ),
    );
  }

  void loadClass(String className) {
    MirrorSystem mirrorSystem = currentMirrorSystem();
    LibraryMirror lm = mirrorSystem.findLibrary(Symbol(''));
    ClassMirror cm = lm.declarations[Symbol(className)];
  }
}
```

#### Java


```java
public final class DexClassLoaderCall extends Loader {

    private static final String TAG = DexClassLoaderCall.class.toString();

    @Override
    public String getDescription() {
        return "Use of dex class load";
    }

    @Override
    public void run() throws Exception {
        /*
            Dex class loading from external storage
         */
        String apkFile = Environment.getExternalStorageDirectory().getAbsolutePath() + "/app.apk";
        DexClassLoader classLoader1 = new DexClassLoader(
                apkFile,
                apkFile,
                apkFile,
                ClassLoader.getSystemClassLoader());
        classLoader1.loadClass("a.b.c");

        /*
            Dex class loading from hard-coded sdcard path
         */
        DexClassLoader classLoader2 = new DexClassLoader(
                "/sdcard/test.apk",
                "/sdcard/test.apk",
                "/sdcard/test.apk",
                ClassLoader.getSystemClassLoader());
        classLoader2.loadClass("a.b.c");

    }
}
```
