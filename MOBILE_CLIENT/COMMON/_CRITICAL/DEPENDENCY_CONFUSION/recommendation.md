NPM packages offer the possibility to set scopes to packages. Scoped packages on the public npm registry may only be published by the user or organization associated with it, and packages within that scope may be made private. Also, scope names can be linked to a given registry.

```javascript
{
  "name": "@ostorlab/dep1",
  "version": "1.2.3",
  "description": "Scoped dependency 1",
  "dependencies": {
    "@ostorlab/dep2": "1.2.3"
  }
}
```

The used scope must be created beforehand to ensure an attacker can't take it over. To create a public scope, apply the following instructions: https://docs.npmjs.com/creating-an-organization

Scoped registry can be configured by including a similar line in the `.npmrc` file:

```javascript
@ostorlab:registry = https://reg.ostorlab.internal/
```

