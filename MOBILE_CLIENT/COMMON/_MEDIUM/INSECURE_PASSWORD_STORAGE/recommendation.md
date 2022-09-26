Mobile applications must use secure API to store credentials. Android applications may `AccountManager` to store account
credentials. It also highly recommended for mobile application to use OAuth-based authentication to avoid storing
credentials and prevent attacks like password reuse.

To implement OAuth-based authentication, Cordova application may use the `jquery-cordova-oauth2` library. Android
application may use `AccountManager` API and iOS application may use `OAuth2Client` library.