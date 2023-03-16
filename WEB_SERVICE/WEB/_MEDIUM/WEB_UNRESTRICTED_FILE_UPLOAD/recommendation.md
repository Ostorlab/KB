Recommendation to limit and prevent unrestricted file upload:

* The file types allowed to be uploaded should be restricted to only those that are necessary for business
  functionality.
* Never accept a filename and its extension directly without having a whitelist filter.
* The application should perform filtering and content-checking of any files uploaded to the server. Files
  should be thoroughly scanned and validated before being made available to other users. If in doubt, the file should be
  discarded.
* It is necessary to have a list of only permitted extensions on the web application. And file extensions can be
  selected from the list. For instance, it can be a “select case” syntax (in the case of having VBScript) to choose the
  file
  extension regarding the actual file extension.
* All control and Unicode characters should be removed from the filenames and extensions. Also, the special characters
  such as `;`, `:`, `>`, `<`, `/` ,`\`, additional `.`, `*`, `%`, `$`, and so
  on should be discarded as well. If it is applicable and there is no need to have Unicode characters, it is highly
  recommended only to accept Alpha-Numeric characters and only one dot as an input for the file name and the extension;
  in which the file name and also the extension should not be empty at all (regular
  expression: `[a-zA-Z0-9]{1,200}\.[a-zA-Z0-9]{1,10}`).
* Limit the filename length. For instance, the maximum length of the name of a file plus its extension should be less
  than 255 characters (without any directory) in an NTFS partition.
* It is recommended to use an algorithm to determine the filenames. For instance, a filename can be an MD5 hash of the
  name of the file plus the date of the day.
* Uploaded directory should not have any execute permission, and all the script handlers should be removed from these
  directories.
* Limit the file size to a maximum value to prevent denial of service attacks (on file space or another web
  application’s functions, such as the image resizer).
* Restrict small files as they can lead to denial of service attacks. So, the minimum size of files should be
  considered.
* Use Cross-Site Request Forgery protection methods.
* Prevent overwriting a file in case of having the same hash for both.
* Use a virus scanner on the server (if applicable). Or, if the contents of files are not confidential, a free
  virus scanner website can be used. In this case, the file should be stored with a random name and without any
  extension on the server first. Then, after the virus checking (uploading to a free virus scanner website and getting the
  result), it can be renamed to its specific name and extension.
* Use the `POST` method instead of `PUT` or `GET`
* Log users’ activities. However, the logging mechanism should be secured against log forgery and code injection.
* In case of having compressed file extract functions, contents of the compressed file should be checked one by one as a
  new file.
* If possible, consider saving the files in a database rather than on the filesystem.
* If files should be saved in a filesystem, consider using an isolated server with a different domain to serve the
  uploaded files.
* File uploaders should be only accessible to authenticated and authorized users if possible.
* Write permission should be removed from files and folders other than the upload folders. The upload folders should not
  serve any
* Ensure that configuration files such as `.htaccess` or `web.config` cannot be replaced using file uploaders. Ensure
  that appropriate settings are available to ignore the `.htaccess` or `web.config` files if uploaded in the upload
  directories.
* Ensure that files with double extensions (e.g., `file.php.txt`) cannot be executed, especially in Apache.
* Ensure that unauthorized users cannot access uploaded files.
* Adding the `Content-Disposition: Attachment` and `X-Content-Type-Options: nosniff` headers to the response of static
  files will secure the website against Flash or PDF-based cross-site content-hijacking attacks. It is recommended that
  this practice be performed for all of the files that users need to download in all the modules that deal with a file
  download. Although this method does not fully secure the website against attacks using Silverlight or similar
  objects, it can mitigate the risk of using Adobe Flash and PDF objects, especially when uploading PDF files is
  permitted.
* Flash/PDF (`crossdomain.xml`) or Silverlight (`clientaccesspolicy.xml`) cross-domain policy files should be removed
  if they are not in use and there is no business requirement for Flash or Silverlight applications to communicate with
  the website.
* Browser caching should be disabled for the `crossdomain.xml` and `clientaccesspolicy.xml` files. This enables the
  website
  to easily update the file or restrict access to the Web services if necessary. Once the client access policy file is
  checked, it remains in effect for the browser session, so the impact of non-caching to the end-user is minimal. This
  can be raised as a low or informational risk issue based on the content of the target website and the security and
  complexity of the policy file(s).
* CORS headers should be reviewed to only be enabled for static or publicly accessible data. Otherwise, the
  `Access-Control-Allow-Origin` header should only contain authorized addresses. Other CORS headers such as
  `Access-Control-Allow-Credentials` should only be used when they are required. Items within the CORS headers such
  as “Access-Control-Allow-Methods” or `Access-Control-Allow-Headers` should be reviewed and removed if they are not
  required.
