The Apollo GraphQL SQLite normalized cache is constructed with the standard plaintext `SqlNormalizedCacheFactory(context, name)` factory, which accepts only a `Context` and a database file name (e.g. `apollo.db`) and no passphrase, `SupportFactory`, or `SQLiteDatabase.Factory` argument. As a result, normalized GraphQL responses (which frequently contain PHI/PII such as treatment status, care plans, appointments, assessment results, messages, provider names, and in some call sites credentials such as a user passcode supplied as a GraphQL query variable) are persisted at rest in a cleartext SQLite database under the application private data directory.

No `SQLCipher`, `net.zetetic.database.sqlcipher`, `io.realm`, `SupportFactory`, `EncryptedFile`, or other encryption layer is applied between the Apollo cache and the disk. In Apollo Kotlin v3, the cache interceptor writes every successful network response to the normalized store regardless of the configured read `FetchPolicy` (including `NetworkOnly`), unless a `doNotStore` cache header is set; when no such header or cache-key exclusion is configured for credential-bearing operations, the credential value flows unchanged into the persisted record.

The database file itself is created with default `MODE_PRIVATE` (`0600`) permissions under the application UID, which blocks ordinary inter-app access on a non-rooted, non-debuggable device. However, the cleartext file remains recoverable by an attacker with local or physical access: via `adb shell run-as` on debuggable build types (which are sometimes distributed to production), and via root or full-disk forensic extraction on any build type. Standard `adb backup` is only mitigated when `android:allowBackup="false"` is set, which provides no protection against `run-as` or root.

```kotlin
// Vulnerable construction: plaintext SQLite cache, no passphrase / no SQLCipher.
val memoryFirstThenSqlCacheFactory =
    MemoryCacheFactory(maxSizeBytes = MEM_CACHE_SIZE)
        .chain(SqlNormalizedCacheFactory(context, "apollo.db"))

return ApolloClient.Builder()
    .serverUrl("$apiUrl/graphql")
    .okHttpClient(Okhttp.client)
    .normalizedCache(
        normalizedCacheFactory = memoryFirstThenSqlCacheFactory,
        cacheResolver = PhyseraCacheKeyResolver,
        writeToCacheAsynchronously = true,
    )
    .build()
```

A credential-bearing operation whose variable is persisted to the cleartext cache:

```graphql
query CheckPasscode($password: String!) {
    viewer {
        id
        checkPassword(password: $password)
    }
}
```
