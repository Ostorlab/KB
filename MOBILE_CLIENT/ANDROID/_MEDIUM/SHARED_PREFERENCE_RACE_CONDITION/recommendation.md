Do not reuse a single `SharedPreferences.Editor` instance across mutations. Create a fresh editor per mutation so each `commit()`/`apply()` flushes only that call's staged value, and serialize the token read/write surface behind a concurrency primitive.

=== "Java"
	```java
      SharedPreferences sharedPreferences = getSharedPreferences("MyPreferences", Context.MODE_PRIVATE);
      // Fresh editor per mutation - never cache the editor in a shared field.
      sharedPreferences.edit().putString("oauth_token", token).commit();
      sharedPreferences.edit().remove("oauth_token").commit(); // logout
    ```

=== "Kotlin"
	```kotlin
      // Fresh editor per mutation.
      sharedPrefs.edit().putString(OAUTH_TOKEN_KEY, token).commit()
      // Serialize the token read/write surface, e.g. with a Mutex, and expose the token
      // through a hot StateFlow so per-request readers always read the latest value atomically.
      private val tokenLock = Mutex()
      private val _oauthToken = MutableStateFlow("")
      override var oauthToken: String
          get() = _oauthToken.value
          set(value) = runBlocking { tokenLock.withLock { _oauthToken.value = value; set(OAUTH_TOKEN_KEY, value) } }
    ```
