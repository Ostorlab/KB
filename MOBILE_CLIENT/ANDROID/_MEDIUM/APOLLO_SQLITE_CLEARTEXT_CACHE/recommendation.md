Encrypt the Apollo normalized cache at rest, and stop credentials from reaching the cache.

**1. Encrypt the SQLite cache at rest (primary control).** Replace the plaintext factory with Apollo's SQLCipher variant, declaring `com.apollographql.apollo3:apollo-normalized-cache-sqlite-sqlcipher` (plus `net.zetetic:android-database-sqlcipher`) and constructing the factory with a passphrase derived from an Android Keystore-backed key (never a hardcoded literal). This neutralizes `run-as`, root, and forensic extraction regardless of `debuggable`/`allowBackup`, because the recovered file is unreadable without the Keystore key.

```kotlin
val passphrase = keystoreBackedKey()   // 32-byte key from AndroidKeyStore
val sqlCipherFactory = SqlNormalizedCacheFactory(context, "apollo.db", passphrase)
val memoryFirstThenSqlCacheFactory =
    MemoryCacheFactory(maxSizeBytes = MEM_CACHE_SIZE).chain(sqlCipherFactory)
```

**2. Suppress credential caching.** Set `ApolloCacheHeaders.DO_NOT_STORE` / `doNotStore(true)` on any credential-bearing operation (such as a passcode check) so the cache interceptor skips `writeOperation()` and the credential is never persisted, even in the encrypted store.

**3. Shred the cache file on logout.** Replace the row-only `apolloStore.clearAll()` (which only issues `DELETE FROM records` and leaves the file, WAL, and unvacuumed pages intact) with `context.deleteDatabase("apollo.db")` plus client recreation, and add a crash-safe startup guard that wipes a stale cache when the prior logout was interrupted.

**4. Harden build types.** Set `isDebuggable = false` on distributed build types (`prod`/`staging`/`dev`) and add a CI gate that fails the build when debuggable is enabled on released flavors. Keep `android:allowBackup="false"`; treat it as defense-in-depth only, not a substitute for encryption.

**5. Cache key hygiene.** In the cache key resolver, strip or hash sensitive variables before computing cache keys, so that sensitive argument values do not flow unchanged into persisted record keys or values.
