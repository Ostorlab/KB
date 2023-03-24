If `Stack canary` is missing, Compilers such as GCC enable this feature if requested through compiler options:

* `-fstack-protector`: Check for stack smashing in functions with vulnerable objects. This includes functions with buffers larger than 8 bytes or calls to `alloca`.
* `-fstack-protector-strong`: Like `-fstack-protector`, but also includes functions with local arrays or references to local frame addresses.
* `-fstack-protector-all`: Check for stack smashing in every function.