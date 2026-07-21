To mitigate the missing revocation and rotation on the JWT refresh endpoint, wire a server-side token-tracking store and enforce rotation semantics, in addition to tightening the token lifetime. The remediation is shown for the `drf-jwt` library but applies to any stateless JWT refresh implementation.

### Immediate mitigation

- **Wire the drf-jwt blacklist app** to enable server-side revocation. Add `rest_framework_jwt.blacklist` to `INSTALLED_APPS` in every settings file and run migrations, so the `apps.is_installed('rest_framework_jwt.blacklist')` revocation gate becomes live and stolen tokens can be revoked before `exp`.
- **Set an explicit `JWT_AUTH` dict** to shorten the replay window until rotation is fully implemented.
- **Remove any committed `SECRET_KEY` fallback** in dev/ci/test and require the environment variable with a fail-closed `ImproperlyConfigured`, eliminating the forgery precondition that chains into this endpoint.

### Permanent fix

Override the refresh serializer/view to implement rotation semantics: mark the consumed token's `jti`/`orig_jti` as outstanding or blacklisted before minting the new token, and acquire a `select_for_update` lock on the outstanding-token row to defeat concurrent-refresh races.

Below are examples of secure configuration and rotation-enforcing code:

=== "Django / drf-jwt"

    ```python
    # ostorlab/settings_dev.py — explicit JWT_AUTH + blacklist wired.
    import datetime

    JWT_AUTH = {
        "JWT_ALGORITHM": "HS256",
        "JWT_VERIFY": True,
        "JWT_VERIFY_EXPIRATION": True,
        "JWT_EXPIRATION_DELTA": datetime.timedelta(minutes=5),
        "JWT_ALLOW_REFRESH": True,
        "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(hours=1),
        "JWT_TOKEN_ID": "include",
        "JWT_SECRET_KEY": os.environ["JWT_SECRET_KEY"],  # independent, env-only.
    }

    INSTALLED_APPS = [
        # ...
        "rest_framework.authtoken",
        "rest_framework_jwt.blacklist",  # <-- ADD: activates revocation gate.
    ]
    ```

    ```python
    # ostorlab/settings_dev.py — env-only SECRET_KEY, fail-closed.
    SECRET_KEY = os.environ["SETTINGS_SECRET_KEY"]
    ```

    ```python
    # apis/views.py — refresh view with rotation + concurrency lock.
    from rest_framework_jwt import views as jwtviews
    from rest_framework_jwt.blacklist.models import OutstandingToken
    from rest_framework_jwt.serializers import RefreshAuthTokenSerializer


    class RotatingRefreshJSONWebTokenView(jwtviews.RefreshJSONWebTokenView):
        serializer_class = RefreshAuthTokenSerializer

        def post(self, request, *args, **kwargs):
            # Mark the consumed token as outstanding/blacklisted before minting
            # the new token; select_for_update defeats concurrent-refresh races.
            with transaction.atomic():
                jti = ...  # extract jti/orig_jti from the presented token
                OutstandingToken.objects.select_for_update().filter(
                    jti=jti
                ).update(blacklisted=True)
            return super().post(request, *args, **kwargs)
    ```

    ```python
    # apis/urls.py — wire the rotating refresh view.
    urlpatterns = [
        re_path(r"^jwt-token/", jwtviews.obtain_jwt_token, name="jwt_token"),
        re_path(
            r"^jwt-token-refresh/",
            RotatingRefreshJSONWebTokenView.as_view(),
            name="jwt_token_refresh",
        ),
    ]
    ```

### Verification

- Static: confirm `grep -rn 'JWT_AUTH' ostorlab/settings_*.py` returns the dict in every environment; confirm `grep -rn 'rest_framework_jwt.blacklist' ostorlab/settings_*.py` returns it inside `INSTALLED_APPS`; confirm `grep -rn 'SETTINGS_SECRET_KEY' ostorlab/settings_dev.py` shows no committed fallback literal.
- Dynamic: obtain a valid JWT, call `POST /apis/jwt-token-refresh/` twice concurrently with the same token, then attempt to use the original token against an authenticated endpoint. After the fix the original must be rejected (blacklisted), confirming rotation and race protection.
- Confirm `python manage.py migrate rest_framework_jwt.blacklist` creates the `BlacklistedToken` table and that revoking a token via the blacklist admin/serializer causes authenticated requests with that token to fail before `exp`.
