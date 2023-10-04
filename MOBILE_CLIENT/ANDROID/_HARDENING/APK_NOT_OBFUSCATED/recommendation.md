Design the application to add the following protections and slow reverse engineering of the application:

* Obfuscate Java source code with tools like Proguard.

=== "Gradle"
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

=== "Gradle"
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

* Verification application signing certificate during runtime by checking `context.getPackageManager().signature`
* Check application installer to ensure it matches the Android Market by calling `context.getPackageManager().getInstallerPackageName`
* Check running environment at runtime

=== "Java"
	```java
    private static String getSystemProperty(String name) throws Exception {
        Class systemPropertyClazz = Class.forName("android.os.SystemProperties");
        return (String) systemPropertyClazz.getMethod("get", new Class[] { String.class }).invoke(systemPropertyClazz, new Object[] { name });
    }
    
    public static boolean checkEmulator() {
    
        try {
            boolean goldfish = getSystemProperty("ro.hardware").contains("goldfish");
            boolean qemu = getSystemProperty("ro.kernel.qemu").length() > 0;
            boolean sdk = getSystemProperty("ro.product.model").equals("sdk");
    
            if (qemu || goldfish || sdk) {
                return true;
            }
    
        } catch (Exception e) {}

        return false;
    }
	```



* Check debug flag at runtime

=== "Java"
	```java
	    context.getApplicationInfo().applicationInfo.flags & ApplicationInfo.FLAG_DEBUGGABLE;
	```
