A stateless JSON Web Token (JWT) refresh endpoint mints a fresh access token from a presented JWT without invalidating, rotating, or revoking the original token. Because the verification path performs only signature and `exp` checks against a stateless default configuration, there is no server-side outstanding-token store, no blacklist, and no rotation logic. This produces three coupled lifecycle weaknesses:

- **Token replay**: a stolen or leaked JWT remains valid until its own `exp` with no server-side replay detection or revocation possible.
- **Non-rotation on refresh**: refresh mints a new token but does NOT invalidate the original; both old and new tokens are independently valid until their respective `exp`.
- **Concurrent-refresh race**: two concurrent refresh requests carrying the same valid JWT both pass verification and both mint an independently valid token, because there is no lock, nonce, or outstanding-token table.

The `jti`/`orig_jti` claims may be generated and propagated across refresh, but if no outstanding/blacklist store is wired these claims are purely decorative. The weakness is rated **Medium** standalone as it requires a stolen or forged token precondition, but it can elevate to **High/Critical** when chained with a committed or leaked signing secret that lets an attacker forge an HS256 JWT and have the refresh endpoint convert the short-lived forged token into a long-lived, self-renewing server-signed session.

Below is an example of an insecure configuration using the `drf-jwt` library, where the refresh route is the stock `refresh_jwt_token` view, no `JWT_AUTH` settings override exists, and the optional `rest_framework_jwt.blacklist` revocation app is absent from `INSTALLED_APPS`:

=== "Django / drf-jwt"

    ```python
    # apis/urls.py — refresh endpoint is the unmodified stock drf-jwt view.
    from django.urls import re_path
    from rest_framework_jwt import views as jwtviews

    urlpatterns = [
        re_path(r"^jwt-token/", jwtviews.obtain_jwt_token, name="jwt_token"),
        re_path(
            r"^jwt-token-refresh/",
            jwtviews.refresh_jwt_token,
            name="jwt_token_refresh",
        ),
    ]
    ```

    ```python
    # ostorlab/settings_dev.py — no JWT_AUTH dict, blacklist app NOT wired.
    INSTALLED_APPS = [
        # ...
        "rest_framework.authtoken",
        # 'rest_framework_jwt.blacklist',  # <-- MISSING: revocation gate is dead code.
    ]

    # No JWT_AUTH override: drf-jwt built-in stateless defaults apply:
    #   JWT_ALLOW_REFRESH = True
    #   JWT_EXPIRATION_DELTA = 300s
    #   JWT_REFRESH_EXPIRATION_DELTA = 7 days
    ```

    ```python
    # ostorlab/settings_dev.py — committed SECRET_KEY fallback (enables forgery chain).
    SECRET_KEY = os.environ.get(
        "SETTINGS_SECRET_KEY",
        "0!gurh&^=h(01^hti-ewkyx658xzs^t4=t-v$kba1f^3#m-i1@",
    )
    # JWT_SECRET_KEY resolves to settings.SECRET_KEY, so a forged HS256 JWT
    # signed with this committed key passes refresh verification and is
    # converted into a long-lived server-signed token.
    ```

The same anti-pattern applies to any stateless JWT refresh implementation (custom or library-provided) that verifies a presented token with signature + `exp` checks only, mints a new token preserving `orig_iat`/`orig_jti`, and performs no blacklist, delete, or outstanding-marking call against the consumed token.
