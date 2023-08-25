Implement biometric authentication with `CryptoObject` usage.

The authentication flow would be as follows when using `CryptoObject`:

* The app creates a key in the KeyStore with:
  - `setUserAuthenticationRequired` set to `true`
  - `setInvalidatedByBiometricEnrollment` set to `true`
  - `setUserAuthenticationValidityDurationSeconds` set to `-1`.

=== "Kotlin"
	```kotlin
	val paramsBuilder = KeyGenParameterSpec.Builder(keyName, KeyProperties.PURPOSE_SIGN)
	        paramsBuilder.apply {
	            when {
	                Build.VERSION.SDK_INT >= Build.VERSION_CODES.R -> {
	                    setDigests(KeyProperties.DIGEST_SHA256)
	                    setUserAuthenticationRequired(true)
	                    setAlgorithmParameterSpec(ECGenParameterSpec("secp256r1")) // ECDSA parameter (P-256) curve
	                    setInvalidatedByBiometricEnrollment(true)
	                    setUserAuthenticationParameters(0, KeyProperties.AUTH_BIOMETRIC_STRONG)
	                }
	                Build.VERSION.SDK_INT >= Build.VERSION_CODES.N && Build.VERSION.SDK_INT <= Build.VERSION_CODES.Q -> {
	                    setDigests(KeyProperties.DIGEST_SHA256)
	                    setUserAuthenticationRequired(true)
	                    setAlgorithmParameterSpec(ECGenParameterSpec("secp256r1"))
	                    setInvalidatedByBiometricEnrollment(true)
	                    setUserAuthenticationValidityDurationSeconds(-1)
	                }
	                else -> {
	                    setDigests(KeyProperties.DIGEST_SHA256)
	                    setUserAuthenticationRequired(true)
	                    setAlgorithmParameterSpec(ECGenParameterSpec("secp256r1"))
	                    setUserAuthenticationValidityDurationSeconds(-1)
	                }
	            }
	        }
	```


* The keystore key must be used to encrypt information that is authenticating the user, like session information or authentication token.

* Biometrics are presented before the key is accessed from the KeyStore to decrypt the data. The biometric is validated with `authenticate` method and the `CryptoObject`. This solution cannot be bypassed, even on rooted devices as the keystore key can only be used after successful biometric authentication.

=== "Kotlin"
	```kotlin
	fun showBiometricPrompt(
	        title: String = "Biometric Authentication",
	        subtitle: String = "Enter biometric credentials to proceed.",
	        description: String = "Input your Fingerprint or FaceID
	to ensure it's you!",
	        activity: AppCompatActivity,
	        listener: BiometricAuthListener
	    ) {
	        val promptInfo = setBiometricPromptInfo(title, subtitle, description)
	
	        val biometricPrompt = initBiometricPrompt(activity, listener)
	
	        biometricPrompt.authenticate(
	            promptInfo, BiometricPrompt.CryptoObject(
	                CryptoUtil.getOrCreateSignature()
	            )
	        )
	    }
	```



* If `CryptoObject` is not used as part of the authenticate method, it can be bypassed by using dynamic instrumentation with a debugger or with tools like Frida.