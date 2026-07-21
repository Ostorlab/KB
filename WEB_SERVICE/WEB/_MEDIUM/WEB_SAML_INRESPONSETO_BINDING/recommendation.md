Persist the `AuthnRequest` ID at SSO initiation, pass it into the response-processing routine so the library's `WRONG_INRESPONSETO` guard fires, and enable unsolicited-response rejection in the SP security configuration. Pin the SAML library to a version that honours these controls.

Below are examples of secure configuration across popular SAML stacks:

=== "Django (python3-saml)"

   ```python
   from onelogin.saml2.auth import OneLogin_Saml2_Auth

   def initiate_sso(request, return_to):
       message = auth.login(return_to)
       # Persist the AuthnRequest ID keyed to the session (short TTL).
       request.session["saml_request_id"] = auth.get_last_request_id()
       return redirect(message)

   def acs(request):
       req = prepare_request(request)
       auth = OneLogin_Saml2_Auth(req, old_settings=saml_settings)
       # Pass the persisted request ID -> activates WRONG_INRESPONSETO guard.
       request_id = request.session.get("saml_request_id")
       auth.process_response(request_id=request_id)
       errors = auth.get_errors()
       ...
   ```

   ```python
   # Enable unsolicited-response rejection and InResponseTo binding.
   "security": {
       "wantAttributeStatement": False,
       "requestedAuthnContext": False,
       "wantResponseInResponseTo": True,
       "rejectUnsolicitedResponsesWithInResponseTo": True,
   },
   ```

   ```text
   # requirements.txt - pin to a version honouring the InResponseTo controls.
   python3-saml==1.16.0
   ```

=== "Node.js (passport-saml)"

   ```javascript
   // passport-saml validates InResponseTo against a replay cache when enabled.
   const samlStrategy = new saml.Strategy({
     path: '/saml/acs',
     entryPoint: 'https://idp.example.com/sso',
     // default: validateInResponseTo=true and a request ID replay cache are enabled;
     // do NOT disable them and persist the cache server-side.
   }, (profile, done) => done(null, { email: profile.nameID }));
   ```

=== "Spring Boot (Spring Security SAML)"

   ```java
   @Bean
   public WebSecurityConfigurerAdapter saml() {
       http.apply(samlDsl())
           .securityContext()
           .replayPrevention(true); // enforce InResponseTo replay cache
   }
   ```

Additional hardening:

* Restrict the ACS endpoint at the reverse proxy to the configured IdP source IPs/origins.
* Enable request logging/alerting on accepted ACS events to detect replay bursts.
* Use short assertion `NotOnOrAfter` validity windows at the IdP.
