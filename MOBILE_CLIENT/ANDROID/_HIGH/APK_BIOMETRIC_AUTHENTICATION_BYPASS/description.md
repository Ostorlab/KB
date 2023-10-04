Android provides mechanisms to enforce biometric authentication to protect sensitive information. Biometric authentication has evolved over time to provide improved user experience, developer experience and improved security.

Previous implementation using `FingerprintManager` is deprecated and must not be used. Proper implementation must use`BiometricManager` with `BiometricPrompt` and `CryptoObject`.

`CryptoObject` provides cryptographic primitives for encryption, decryption and signature validation.

In the example below, calling the `authenticate` method without `cryptoObject` is vulnerable to authentication bypass:

=== "Kotlin"
	```kotlin
	fun showBiometricPrompt(
	    title: String = "Biometric Authentication",
	    subtitle: String = "Enter biometric credentials to proceed.",
	    description: String = "Input your Fingerprint or FaceID to ensure it's you!",
	    activity: AppCompatActivity,
	    listener: BiometricAuthListener,
	    cryptoObject: BiometricPrompt.CryptoObject? = null,
	    allowDeviceCredential: Boolean = false
	) {
	  // 1
	  val promptInfo = setBiometricPromptInfo(
	      title,
	      subtitle,
	      description,
	      allowDeviceCredential
	  )
	
	  // 2
	  val biometricPrompt = initBiometricPrompt(activity, listener)
	
	  // 3
	  biometricPrompt.apply {
	    if (cryptoObject == null) authenticate(promptInfo)
	    else authenticate(promptInfo, cryptoObject)
	  }
	}
	```

