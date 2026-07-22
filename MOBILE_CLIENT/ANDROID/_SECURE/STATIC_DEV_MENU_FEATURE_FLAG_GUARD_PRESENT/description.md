The application gates developer-only menu route registration at navigation-graph build time behind a runtime feature flag that resolves to `false` on non-debug (release and pentest) builds.

At composition time the NavHost only registers the dev menu destination when a feature flag evaluates to true, for example:

```kotlin
if (RuntimeBehavior.isFeatureEnabled(FeatureFlag.DEV_MENU_FLAG)) {
    devMenuNavGraph()
}
```

The flag provider set is selected from `BuildConfig.DEBUG` at application initialization. On non-debug builds a hardwired-false provider (e.g. a `StoreFeatureFlagProvider` that always returns `false`) is registered, and the dev-menu feature flag defaults to `false`. As a result the dev menu destination, its composable and the corresponding bottom-navigation tab are never added to the navigation graph on release/pentest builds.

Because the route is never registered, Compose Navigation cannot match it: the dev menu destination passes no `deepLinks=` argument, declares no `deepLinkRoutes`, and no `physera://` (or equivalent app scheme) URI can resolve to it. There is also no gesture, tap-counter or shake activator that opens the dev menu, and no UI reachable on a non-debug build that calls the API server setter, so the API endpoint remains bound at application init from build-variant resources and is not user-controllable.

This means developer tooling is correctly excluded from production builds and cannot be reached without authentication via deep links or hidden gestures on non-debug builds.
