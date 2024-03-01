```
One of the main features of debug mode is the display of detailed error pages.  
If your app raises an exception when DEBUG is True, Django will display a detailed  
traceback, including a lot of metadata about your environment, such as all the  
currently defined Django settings (from settings.py).
```

Debug mode provides developers with detailed information about errors happening in their code.
It displays tracebacks, metadata about the environment, and currently defined Django settings.

This is useful when developing, but gives the attacker information about the used `Django` & `Python`  
versions to match against CVEs, and access to source code snippets, internal file paths, some variables and their values.