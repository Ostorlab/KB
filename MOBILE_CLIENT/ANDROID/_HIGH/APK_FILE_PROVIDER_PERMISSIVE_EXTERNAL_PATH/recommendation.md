* Avoid permissive settings when using `external-path`, like `'.'`.
* Avoid using `root-path`.
* Avoid assign the root path to path attribute `path='/.'`in all paths types.
* You should make sure that you're only sharing files that are necessary and appropriate to share.
* Avoid sharing sensitive files or files that contain sensitive information.
* Ensure that you use the `<grant-uri-permission>` tag to control access to the shared files.
* Prefer `external-files-path`.
* use specific folders for path attribute:

```xml
<?xml version="1.0" encoding="utf-8"?>
<paths>
    <external-path
        name="downloads"
        path="Download/" />
</paths>
```
