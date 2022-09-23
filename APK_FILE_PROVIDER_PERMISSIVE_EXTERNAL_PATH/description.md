The application exposes a file provider using `androidx.core.content.FileProvider`. The provider specifies
available files in the metadata child attribute with the name `android.support.FILE_PROVIDER_PATHS`.

The attribute is required to generate URI for directories specified `android.support.FILE_PROVIDER_PATHS` configuration
file.

Android defines multiple paths types:

```xml
<files-path name="name" path="path" />
```

* Represents files in the files/ subdirectory of your app's internal storage area. This subdirectory is the same as the 
value returned by `Context.getFilesDir()`.

```xml
<cache-path name="name" path="path" />
```

* Represents files in the cache subdirectory of your app's internal storage area. The root path of this subdirectory is 
the same as the value returned by `getCacheDir()`.

```xml
<external-path name="name" path="path" />
```

* Represents files in the root of the external storage area. The root path of this subdirectory is the same as the value
returned by `Environment.getExternalStorageDirectory()`.

```xml
<external-files-path name="name" path="path" />
```

* Represents files in the root of your app's external storage area. The root path of this subdirectory is the same as the
value returned by `Context.getExternalFilesDir(null)`.

```xml
<external-cache-path name="name" path="path" />
```

* files in the root of your app's external cache area. The root path of this subdirectory is the same as the
value returned by `Context.getExternalCacheDir()`.

```xml
<external-media-path name="name" path="path" />
```

* Represents files in the root of your app's external media area. The root path of this subdirectory is the same as the
value returned by the first result of `Context.getExternalMediaDirs()`.
  
The application specifies a permissive `android.support.FILE_PROVIDER_PATHS`.
