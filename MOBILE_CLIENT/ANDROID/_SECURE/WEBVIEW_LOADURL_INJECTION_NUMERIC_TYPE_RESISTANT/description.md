The application loads a URL in a `WebView` using `loadUrl` where the query parameter values are
interpolated from numeric-typed values (`Int`, `Long`, `Double`, or `Float`) rather than from
attacker-controlled `String` input. The static type system constrains the values end-to-end from
their origin to the `toString()` interpolation at the sink, so the rendered URL cannot carry
script-delimiting characters into the browser context.

This makes the named client-side parameter-injection / cross-site scripting (XSS) vector
unreachable through the `loadUrl` path:

- Kotlin/Java `Int.toString()` emits only `[-]?[0-9]+`; `Long.toString()` is equivalent.
- `Double.toString()` / `Float.toString()` emit only digits, `.`, `E`/`e`, `-` (plus the
  specials `NaN`, `Infinity`, `-Infinity`).
- Neither can produce `<`, `>`, `"`, `'`, space, `/`, `;`, `=`, `(`, `)`, or newline — the
  characters required to break out of a URL query value into HTML/script context.
- An example `<script>...</script>` payload is therefore unconstructible through this path,
  including for malformed or out-of-range inputs.

### Effective control

The effective control is the numeric primitive type, enforced end-to-end from the data source
(for example an authenticated API/GraphQL scalar) through the repository and view-model layers
down to the string-template interpolation sink. The values do not originate from
attacker-supplied HTTP parameters, intent extras, or deep-link parameters, and no
`String`-typed alias or mutable reassignment feeds these fields.

### Residual (not-assessable) surface

The only residual XSS surface is server-side reflection of the query parameters by the rendered
page. This is independent of the client-side numeric type constraint and cannot be assessed from
the mobile application code alone.
