Narrow the ProGuard/R8 keep rules so R8 can rename sensitive model classes and fields, and keep only the members that genuinely require their original names at runtime. Replace package-wide keeps with targeted, annotation- or member-driven rules.

### Step 1 — Annotate fields that depend on their Kotlin/Java name as the wire key

For reflection-based JSON libraries (such as Klaxon) that fall back to the property name when no override is present, give every serialized field an explicit annotation that fixes the wire name independently of the obfuscated identifier:

```kotlin
@Json(name = "username") val username: String,
@Json(name = "password") val password: String,
@Json(name = "token") val token: String,
```

Use the exact wire names the server expects. Once every serialized field carries an explicit name, serialization correctness no longer depends on the Kotlin property identifier.

### Step 2 — Delete the broad package-wide keep rules

Remove rules that retain an entire model package tree:

```proguard
# DELETE these overly broad rules:
# -keep class com.example.app.api.models.** { *; }
# -keep class com.example.app.**models.** { *; }
```

### Step 3 — Rely on targeted, annotation-driven rules instead

Keep only the members that truly need their original names. The annotation-driven rule below preserves the fields that carry a JSON annotation while letting R8 rename everything else:

```proguard
-keepclassmembers class * {
    @com.beust.klaxon.Json <fields>;
}
```

For kotlinx.serialization the serial names are baked into the generated `$serializer` as compile-time string constants, so renaming the Kotlin property does not change the wire key and no extra keep rule is required. For Apollo GraphQL, fields are resolved through compile-time generated accessors rather than reflection on the wrapper property names, so the model wrappers can be safely renamed.

### Step 4 — Verify

1. Build the release APK: `./gradlew :app:assembleRelease`.
2. Decompile the APK with JADX or Apktool.
3. Confirm that the sensitive model field names no longer appear as class field names and that the model classes are renamed to short identifiers.
4. Re-run the REST flows whose fields were annotated to confirm the wire format is unchanged.
5. Re-run the GraphQL queries to confirm response mapping still works through the compile-time accessors.
