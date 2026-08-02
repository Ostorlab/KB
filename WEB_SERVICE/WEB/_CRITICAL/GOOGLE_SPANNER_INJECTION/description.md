Google Spanner injection is a security vulnerability that occurs when attackers exploit weaknesses in applications using Google Cloud Spanner. It involves injecting malicious or unexpected data into input fields, enabling attackers to manipulate the Spanner SQL statements executed by the application and access unauthorized information.

Similar to SQL injection attacks against traditional SQL databases, Spanner injection targets applications using Google Cloud Spanner. Spanner exposes a SQL interface whose queries are constructed by the application. When user-supplied values are concatenated directly into the SQL statement string passed to the Spanner client instead of being bound as parameters, an attacker can craft input to alter the logic of the query, bypass authentication, or retrieve sensitive information stored in the database. Spanner injection attacks can lead to unauthorized data access, data modification, or the complete compromise of the data stored in the database, compromising the confidentiality, integrity, and availability of the application and its data.


### Examples

=== "Java"

  ```java
  import com.google.cloud.spanner.*;
  import org.springframework.web.bind.annotation.*;

  @RestController
  @RequestMapping("/login")
  public class SpannerInjectionController {

      @PostMapping
      public void login(@RequestParam String userName, @RequestParam String password) throws Exception {
          SpannerOptions options = SpannerOptions.newBuilder().build();
          try (Spanner spanner = options.getService()) {
              DatabaseId dbId = DatabaseId.of("my-project", "my-instance", "my-database");
              DatabaseClient client = spanner.getDatabaseClient(dbId);

              // Vulnerable query susceptible to Spanner Injection
              String sql = "SELECT * FROM users WHERE username = '" + userName
                      + "' AND password = '" + password + "'";

              try (ResultSet rs = client.singleUse().executeQuery(Statement.of(sql))) {
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

      // Vulnerable query susceptible to Spanner Injection
      const sql = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;

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

      # Vulnerable query susceptible to Spanner Injection
      sql = (
          f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
      )

      with database.snapshot() as snapshot:
          results = snapshot.execute_sql(sql)
          rows = list(results)

      return {"success": len(rows) > 0}
  ```
