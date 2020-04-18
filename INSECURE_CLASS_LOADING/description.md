Android provides APIs that allow an application to dynamically load code to be executed. For example, an application may support plug-ins that are downloaded and then loaded at a later time. Unfortunately, if these plug-ins are stored in an insecure location, this process can be hijacked, allowing access to private data and unexpected arbitrary code execution by malicious applications

Two classes allow the loading of additional code:
```java
    DexClassLoader (String dexPath, String dexOutputDir, String libPath, ClassLoader parent)
```
```java
    PathClassLoader (String path, String libPath, ClassLoader parent)
```