To output log messages to <code>LogCat</code> in a safe manner, pursue the following recommendations:

* Sensitive information must not be included in operation log information. Construct the build system to Auto-delete
  codes which output development log information: For example, `Log.d()` and `Log.v()` should be deleted when building
  an application for release. ProGuard is a tool that can automatically delete them by specifying `Log.d()` and `Log(v)`
  as parameter of `-assumenosideeffects` option.
* Use `Log.d()` or `Log.v()` when Outputting throwable Objects: When exceptions occur, stack trace is often output
  to `LogCat` by `Log.e()`, `Log.w()` or `Log.i()` methods. Thus, detail internal structure can be shown. For example,
  when SQLiteException is output as it is, type of SQL statement is revealed and it may give a clue for SQL injection
  attack.
* Use only Methods of the `android.util.Log` class for Log Output.
* Do not output log information using `print()` or `println()` method of `System.out` and `System.err` class since log
  information and development log information are output by the same method and it fosters the danger of dropped
  deletion by oversight. Moreover, using both `android.util.Log` and `System.out/err` will increase considered needs
  and, as a result the danger of occurring mistakes will increase.
* Choose the right log level based on the information criticity. ( ERROR, WARN, INFO, DEBUG, VERBOSE )
