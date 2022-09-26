- Sending the proper X-Frame-Options in HTTP response headers instructing the browser not to allow framing from other
  domains.
    - `X-Frame-Options: DENY`  It completely denies being loaded in frame/iframe.
    - `X-Frame-Options: SAMEORIGIN` allows only if the site which wants to load has the same origin.
    - `X-Frame-Options`: ALLOW-FROM URL grants a specific URL to load itself in an iframe. However, please pay
      attention to that; not all browsers support this.
- Employing defensive code in the UI to ensure that the current frame is the top-level window.
