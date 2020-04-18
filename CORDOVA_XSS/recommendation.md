The application must validate all provided input and use secure HTML formating API. The recommended approach is defining a list of acceptable characters and allow only those characters. Acceptable characters would be upper case letters, lower case letters, and numbers (i.e. `a-z`, `A-Z`, and `0-9`).

Frameworks offer methods to validate input and prevent XSS vulnerabilities and modern frameworks (Angular JS 2, React JS) automatically escapes user input:

To escape input using Sencha Ext JS, the following methods could be used:

*   `Ext.util.Format.stripTags`
*   `Ext.util.Format.stripScripts`
*   `Ext.util.Format.htmlEncode/Decode`