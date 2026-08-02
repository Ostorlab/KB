To prevent Google Spanner injection attacks, consider the following measures:

- __Use Parameterized Queries__: Always bind user-supplied values as parameters to the Spanner statement instead of concatenating them into the SQL string. The Spanner client libraries support `?` placeholders (or named `@param` placeholders) that are bound through `Statement.newBuilder(...).bind(...)` in Java, the `params` option of `database.run` in Node.js, and the `params`/`param_types` arguments of `snapshot.execute_sql` in Python. Bound values are treated strictly as data and never as part of the SQL syntax.

- __Input Validation and Sanitization__: Implement robust input validation to ensure that user-supplied data meets expected formats and types. Use sanitization techniques such as whitelisting acceptable characters to reject unexpected input. Validation is a defence-in-depth measure and must not replace parameterization.

- __Least-Privilege Database Accounts__: Connect to Spanner using database roles or IAM principals that are scoped to the minimum permissions the application needs. This limits the impact of a successful injection by restricting the operations an attacker can perform through the injected query.

### Examples

=== "Java"

  ```java
  import com.google.cloud.spanner.*;
  import org.springframework.web.bind.annotation.*;

  @RestController
  @RequestMapping("/login")
  public class SecureSpannerInjectionController {

      @PostMapping
      public void login(@RequestParam String userName, @RequestParam String password) throws Exception {
          SpannerOptions options = SpannerOptions.newBuilder().build();
          try (Spanner spanner = options.getService()) {
              DatabaseId dbId = DatabaseId.of("my-project", "my-instance", "my-database");
              DatabaseClient client = spanner.getDatabaseClient(dbId);

              // Secure query using parameterization to prevent Spanner Injection
              Statement statement = Statement.newBuilder(
                      "SELECT * FROM users WHERE username = @username AND password = @password")
                      .bind("username").to(userName)
                      .bind("password").to(password)
                      .build();

              try (ResultSet rs = client.singleUse().executeQuery(statement)) {
                  while (rs.next()) {
                      System.out.println(rs.getString("username"));
                  }
              }
          }
      }
  }
  ```

=== "JavaScript"

  ```javascript
  const { Spanner } = require('@google-cloud/spanner');
  const express = require('express');
  const app = express();

  app.use(express.json());

  app.post('/login', async (req, res) => {
      const username = req.body.username;
      const password = req.body.password;

      const spanner = new Spanner({ projectId: 'my-project' });
      const instance = spanner.instance('my-instance');
      const database = instance.database('my-database');

      // Secure query using parameterization to prevent Spanner Injection
      const sql = {
          sql: 'SELECT * FROM users WHERE username = @username AND password = @password',
          params: {
              username: username,
              password: password,
          },
      };

      try {
          const [rows] = await database.run(sql);
          res.json({ success: rows.length > 0 });
      } finally {
          await database.close();
      }
  });

  app.listen(3000, () => {
      console.log('Server started on port 3000');
  });
  ```

=== "Python"

  ```python
  from google.cloud import spanner
  from flask import Flask, request

  app = Flask(__name__)


  @app.post("/login")
  def login():
      username = request.form.get("username")
      password = request.form.get("password")

      client = spanner.Client()
      instance = client.instance("my-instance")
      database = instance.database("my-database")

      # Secure query using parameterization to prevent Spanner Injection
      sql = "SELECT * FROM users WHERE username = @username AND password = @password"
      params = {"username": username, "password": password}
      param_types = {
          "username": spanner.param_types.STRING,
          "password": spanner.param_types.STRING,
      }

      with database.snapshot() as snapshot:
          results = snapshot.execute_sql(sql, params=params, param_types=param_types)
          rows = list(results)

      return {"success": len(rows) > 0}
  ```
