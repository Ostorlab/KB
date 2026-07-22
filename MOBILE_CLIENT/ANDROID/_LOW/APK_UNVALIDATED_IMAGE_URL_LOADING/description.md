Image URLs supplied by server-controlled content (such as survey `<img>` elements, markdown `![](url)`, `Article.imageUrl` fields, story image fields, or any remote asset URL received from a backend) are passed directly to image loading libraries (for example Coil, Glide or Picasso) without any URL validation. No scheme allowlist, host allowlist, or private/loopback/link-local address blocklist is applied before the image loader issues the outbound request.

Because the image loader uses its own default, interceptor-free HTTP client (separate from the authenticated API client), the patient OAuth bearer token does not travel with these image requests. The verified, realistic impact is therefore client-side request forgery without credential leakage: an attacker who can influence server image content can make any patient's device issue blind HTTP(S) requests toward arbitrary destinations, including attacker-host request logging, local-network / RFC1918 probing and pre-auth internal-service fingerprinting where reachable from the device network. Responses are decoded as images and are not returned to the attacker, and no script executes, so impact is limited to blind probing.

### Examples

#### Kotlin

```kotlin
val painter = rememberAsyncImagePainter(
    model = ImageRequest.Builder(LocalContext.current)
        .data(imageUrl) // no scheme/IP validation
        .crossfade(true)
        .build()
)
```
