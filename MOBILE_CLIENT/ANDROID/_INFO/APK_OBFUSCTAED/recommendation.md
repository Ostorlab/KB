Design the application to add the following protections and slow reverse engineering of the application:

* Obfuscate Java source code with tools like Proguard or Dexguard

=== "Gradle"
	```gradle
	buildTypes { release { minifyEnabled true proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro' } }
	```



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
	    
	        } catch (Exception e) {
	        }
	    
	        return false;
	      }
	```


* Check debug flag at runtime

=== "Java"
	```java
	    context.getApplicationInfo().applicationInfo.flags & ApplicationInfo.FLAG_DEBUGGABLE;
	```


