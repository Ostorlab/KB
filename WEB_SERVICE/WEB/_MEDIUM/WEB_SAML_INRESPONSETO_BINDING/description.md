The SAML Service Provider (SP) does not bind the assertion consumer response to an outstanding `AuthnRequest` (the `InResponseTo` attribute) nor reject unsolicited or replayed SAML responses. The replay-prevention layer of the SAML Web Single Sign-On flow is therefore structurally disabled: an attacker who captures one legitimate, IdP-signed `SAMLResponse` for a target user can POST it to the assertion consumer service (`/saml/acs/` or equivalent) within the assertion's `NotOnOrAfter` validity window and authenticate as the victim.

The flaw combines three independent absences:

* The ACS handler calls the SAML library's response-processing routine with no `request_id` argument, so the library's `InResponseTo` matching guard (`if in_response_to is not None and request_id is not None`) is structurally `False` and never raises `WRONG_INRESPONSETO`.
* The SP security configuration omits the `wantResponseInResponseTo` / `rejectUnsolicitedResponsesWithInResponseTo` (or equivalent) controls, so unsolicited responses carrying no `InResponseTo` are accepted even under `strict=True`.
* The SSO initiator never persists the `AuthnRequest` ID (`get_last_request_id()`), so even a `process_response(request_id=...)` call would have no server-side store to supply.

Signature, issuer, and audience validation remain enforced, so this is a replay-prevention gap rather than a standalone authentication bypass: the attacker must replay a legitimately signed response captured during a real SSO flow and is bound by the short assertion validity window.

Below are examples of the vulnerable pattern across popular SAML stacks:

=== "Django (python3-saml)"

   ```python
   from onelogin.saml2.auth import OneLogin_Saml2_Auth

   def acs(request):
       req = prepare_request(request)
       auth = OneLogin_Saml2_Auth(req, old_settings=saml_settings)
       # request_id is NOT passed -> the library's InResponseTo guard is disabled.
       auth.process_response()
       errors = auth.get_errors()
       if not errors:
           email = auth.get_nameid().lower()
           user = User.objects.get(email=email)
           django_auth.login(request, user)  # victim session established
       ...
   ```

   ```python
   # SSO initiator: the AuthnRequest ID is never persisted.
   message = auth.login(return_to)
   # get_last_request_id() is never called; nothing stored in session/cache/DB.
   return GenerateSamlRedirectUrl(redirect_url=message)
   ```

   ```python
   # Security dict omits every InResponseTo control.
   "security": {
       "wantAttributeStatement": False,
       "requestedAuthnContext": False,
   },
   ```

=== "Node.js (passport-saml)"

   ```javascript
   const samlStrategy = new saml.Strategy({
     path: '/saml/acs',
     entryPoint: 'https://idp.example.com/sso',
     // InResponseTo is not validated: no requestId persistence / matching.
   }, (profile, done) => {
     // profile.email used to log the user in without replay checks.
     return done(null, { email: profile.nameID });
   });
   ```

=== "Spring Boot (Spring Security SAML)"

   ```java
   @Bean
   public WebSecurityConfigurerAdapter saml() {
       // No InResponseTo replay cache / request-id binding configured.
       http.apply(samlDsl())
           .securityContext()
           .replayPrevention(false); // disabled -> captured responses are accepted
   }
   ```
