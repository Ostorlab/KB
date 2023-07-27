To obfuscate your app, use the flutter build command in release mode with the --obfuscate and --split-debug-info options. The --split-debug-info option specifies the directory where Flutter outputs debug files. In the case of obfuscation, it outputs a symbol map. For example:

```sh
flutter build apk --obfuscate --split-debug-info=/<project-name>/<directory>
```

This `--split-debug-info` refers to the location or directory where flutter outputs the debug files.

The following build targets support the obfuscation process described on above:

* `aar`
* `apk`
* `appbundle`
* `ios`
* `ios-framework`
* `ipa`
* `linux`
* `macos`
* `macos-framework`
* `windows`

Obfuscation is not supported for web apps, but a web app can be minified, which is similar. When you build a release version of a Flutter web app, it is automatically minified.

Once you’ve obfuscated your binary, save the symbols file. You need this if you later want to de-obfuscate a stack trace.

If the flutter app uses native Android code (Java/Kotlin), other options are available:

* Obfuscate Java source code with tools like Proguard.

```gradle
    buildTypes {
            release {
                minifyEnabled true
                proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
            }
        }
```
This tells Gradle to use ProGuard for code obfuscation in the release build. You can then create a "proguard-rules.pro"
file in the app's "app" directory to configure the obfuscation rules.

* Obfuscate Java source code with tools like Dexguard.

```gradle
    buildTypes {
            release {
                minifyEnabled true
                useProguard false
                proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
                dexguard {
                  config 'dexguard-release.cfg'
                }
            }
        }
```
This tells Gradle to use DexGuard for code obfuscation in the release build. You can create a"dexguard-project.txt" file in the app's "app" directory to configure the DexGuard project, and a"dexguard-release.cfg" file to configure the obfuscation for the release build.

By default, when you enable code obfuscation using DexGuard, it will use its own obfuscation rules in addition to any rules specified in the ProGuard configuration file. However, you can disable the use of ProGuard's rules by setting the `useProguard` option to false.


