Custom URL schemes provide a way to reference resources inside an iOS app. Users tapping a custom URL in an email, for
example, launch the application in a specified context. Other apps can also trigger another app to launch it with specific context
data; for example, a photo library app might display a specified image.

URL schemes offer a potential attack vector into iOS app and are by default vulnerable scheme hijacking.
App need to make sure to validate all URL parameters and discard any
malformed URLs. In addition, limit the available actions to those that don’t risk the user’s data. For example, don’t
allow other apps to directly delete content or access sensitive information about the user.
