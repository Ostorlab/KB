* Random numbers play a key role in ensuring unguessable Initialization Vectors generation
* In Android applications, `SecureRandom` class generates random numbers secure enough for use in encryption
* There exists multiple providers, which are the internal SecureRandom class implementations, and their role is to
  provide a hash function
* A Default provider will be selected if not specified
* Crypto Provider was deprecated in Android 7.0 (API level 24) and removed in Android 9.0 (API level 28) due to it's
  unsafe SHA1PRNG algorithm
* It is recommended not to use Crypto Provider
* If Crypto Provider is specified and SecureRandom is used, NoSuchProviderException will always occur in devices running
  Android 9.0
  and higher, and NoSuchProviderException will occur even in devices running Android 7.0 and higher if targetSdkVersion>
  =24
* For this reason, generally, the use of SecureRandom without specifying the provider is recommended

=== "Java"
	```java
	import java.security.SecureRandom;
	[...]
	    SecureRandom random = new SecureRandom();
	    byte [] IV = new byte [128];
	    random.nextBytes(IV);
	    IvParameterSpec ivParams = new IvParameterSpec(iv)
	[...]
	```

