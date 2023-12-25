Remove all symbols and debug data from the application. 

To do so, here are some recommendations:

* Configure the build type to exclude debug information.
* Use [ProGuard](https://www.guardsquare.com/en/products/proguard) to strip native debugging symbols.
* Use the `strip` command to remove symbols from native libraries:
```bash
strip -s <library>
```