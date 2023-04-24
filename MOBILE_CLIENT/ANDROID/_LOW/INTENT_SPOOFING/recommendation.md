To limit one's exposure to this type of attack, developers should avoid exporting components unless the component is
specifically designed to handle requests from untrusted applications. Developers should be aware that declaring an
intent filter will automatically export the component, exposing it to public access. Critical, state-changing actions
should not be placed in exported components. If a single component handles both inter- and intra-application
requests, the developer should consider dividing that component into separate components.

If a component must be exported (e.g., to receive system broadcasts), then the component should dynamically check the
caller's identity prior to performing any operations. Requiring Signature or SignatureOrSystem permissions is an
effective way of limiting a component's exposure to a set of trusted applications. Finally, the return values of
exported components can also leak private data, so developers should check the caller's identity prior to returning
sensitive values.
