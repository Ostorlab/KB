* When using external-path, avoid using permissive settings like '.' as the path.
* Avoid using `root-path`.
* Don't assign the root path '/.' to the path attribute in any type of path.
* Be cautious about what files you share and only share files that are necessary and appropriate.
* Don't share sensitive files or files that contain sensitive information.
* Use the <grant-uri-permission> tag to control access to shared files.
* Prefer using `external-files-path` path type.
* use specific folders for path attribute:

```xml
<?xml version="1.0" encoding="utf-8"?>
<paths>
    <external-path
        name="downloads"
        path="Download/" />
</paths>
```
