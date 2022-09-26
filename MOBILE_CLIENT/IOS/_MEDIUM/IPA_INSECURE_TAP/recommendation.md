If you're developing a new app, you should use HTTPS exclusively. If you have an existing app, you should use HTTPS as
much as you can and create a plan for migrating the rest of your app as soon as possible. In addition, your
communication through higher-level APIs needs to be encrypted using TLS version 1.2 with forwarding secrecy. An error is
thrown if you try to make a connection that doesn't follow this requirement. Finally, if your app needs to request an
insecure domain, you have to specify this domain in your app's `Info.plist` file.
