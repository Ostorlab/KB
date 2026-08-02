Google Bigtable injection is a security vulnerability that occurs when an application constructs Bigtable row-key prefixes, row-key ranges, or filter expressions from untrusted user input without validation. Bigtable is a NoSQL, key-value datastore accessed through the Cloud Bigtable client libraries, where reads are driven by row keys, key ranges, and row filters. An attacker who can influence any of these inputs can manipulate the resulting reads to access rows outside their intended scope, enumerate key spaces, or trigger expensive prefix scans that exhaust backend resources.

Unlike traditional SQL injection, Bigtable has no string query language to escape; the injection surface is the row-key space itself. Bigtable stores data lexicographically sorted by row key and serves reads as prefix scans or inclusive key ranges. When an application builds the prefix or the start/stop keys from user input (for example, a tenant identifier, a username, or a search term) and concatenates it with other key segments, an attacker can craft an input that sorts before, between, or after the intended boundaries and have the Bigtable client return rows that belong to other users or tenants.

A common high-impact variant is the prefix-scan takeover: the application trusts a tenant or user identifier as a row-key prefix and calls `read_rows` with that prefix. By supplying an empty prefix, a short prefix, or a prefix whose trailing separator has been stripped, the attacker widens the scan to cover sibling or parent key ranges, leaking cross-tenant data. A second variant abuses Bigtable `RowFilter` chains (such as `ColumnRangeRegex`, `ValueRegex`, or `Chain` filters) built from user input to read columns or values the application did not intend to expose.

Successful exploitation can lead to unauthorized data access, cross-tenant information disclosure, full keyspace enumeration, and denial of service through deliberately broad scans or expensive filter combinations against the Bigtable instance.



### Examples

=== "Python"

  ```python
  from flask import Flask, request
  from google.cloud import bigtable

  app = Flask(__name__)
  client = bigtable.Client(project="my-project", instance_id="my-instance")
  table = client.instance("my-instance").table("sessions")


  @app.get("/sessions")
  def sessions():
      # Attacker-controlled value used directly as a row-key prefix.
      user_id = request.args.get("user_id", "")

      # No validation: an empty or crafted prefix widens the scan to
      # every session row that sorts under the supplied prefix.
      rows = table.read_rows(row_set_prefix=f"{user_id}#".encode())
      return [row.row_key.decode() for row in rows]
  ```

=== "Java"

  ```java
  import com.google.cloud.bigtable.data.v2.BigtableDataClient;
  import com.google.cloud.bigtable.data.v2.models.Query;
  import com.google.cloud.bigtable.data.v2.models.Row;
  import org.springframework.web.bind.annotation.*;

  @RestController
  @RequestMapping("/sessions")
  public class SessionController {

      private final BigtableDataClient dataClient =
          BigtableDataClient.create("my-project", "my-instance");

      @GetMapping
      public Iterable<Row> sessions(@RequestParam String userId) {
          // The user-controlled value is concatenated into the row-key prefix,
          // letting an attacker read rows belonging to other users.
          Query query = Query.create("sessions")
              .rowPrefix(userId + "#");

          return dataClient.readRows(query);
      }
  }
  ```

=== "Javascript"

  ```javascript
  const express = require('express');
  const { Bigtable } = require('@google-cloud/bigtable');

  const bigtableClient = new Bigtable();
  const table = bigtableClient.instance('my-instance').table('sessions');
  const app = express();

  app.get('/sessions', async (req, res) => {
    const userId = req.query.user_id || '';

    // The attacker-controlled prefix is used without any bounds check.
    const [rows] = await table.getRows({
      prefix: `${userId}#`,
    });

    res.json(rows.map((row) => row.id));
  });

  app.listen(3000, () => {
    console.log('Server started on port 3000');
  });
  ```
