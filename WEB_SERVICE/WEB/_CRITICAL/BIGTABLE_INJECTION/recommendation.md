To prevent Google Bigtable injection attacks, consider the following measures:

- __Bound row-key reads to authenticated identity__: Derive the row-key prefix from the server-side authenticated principal (the caller's tenant ID or user ID resolved from the session), never from request parameters. When a request parameter must drive the read, cross-check it against the caller's identity and reject mismatches.

- __Validate the prefix against an allow-list__: Treat row-key prefixes as trusted, structured data. Validate user-supplied segments against a strict format (a UUID, a known identifier, or an allow-list of acceptable values) before placing them in a row key. Reject empty, overly short, or otherwise malformed prefixes that would widen a scan.

- __Use explicit, closed key ranges__: Prefer an explicit start and stop row key over an open-ended prefix scan. Compute the stop key deterministically from the validated start key so the range covers exactly the rows the caller is allowed to read, and never let user input define the upper bound independently.

- __Avoid user input in row filters__: Do not pass user-controlled values into `RowFilter` chains such as `ColumnRangeRegex`, `ValueRegex`, or `BlockRegex`. If filtering by user input is required, validate the input against a tight allow-list and compile the filter server-side from trusted components.

- __Design row keys for tenant isolation__: Structure row keys so that a single tenant's rows cannot be addressed by widening another tenant's prefix (for example, by prefixing every key with a fixed-width, validated tenant ID and a delimiter). This prevents prefix-scan takeover across tenants.

### Examples

=== "Python"

  ```python
    import uuid

    from flask import Flask, request, session
    from google.cloud import bigtable


    def validate_user_id(raw: str) -> str:
        # Only accept a strict UUID; reject anything that could widen a prefix scan.
        value = str(raw)
        parsed = uuid.UUID(value)  # raises ValueError on malformed input
        return str(parsed)


    app = Flask(__name__)
    client = bigtable.Client(project="my-project", instance_id="my-instance")
    table = client.instance("my-instance").table("sessions")


    @app.get("/sessions")
    def sessions():
        # The caller identity is resolved server-side from the session, not the query.
        tenant_id = session["tenant_id"]
        user_id = validate_user_id(request.args["user_id"])

        prefix = f"{tenant_id}#{user_id}#".encode()
        start = prefix
        # Closed, deterministic stop key: the character after the delimiter
        # bounds the range to exactly this user's rows.
        stop = prefix[:-1] + bytes([prefix[-1] + 1])

        rows = table.read_rows(start_key=start, end_key=stop)
        return [row.row_key.decode() for row in rows]
  ```

=== "Java"

  ```java
    import com.google.cloud.bigtable.data.v2.BigtableDataClient;
    import com.google.cloud.bigtable.data.v2.models.Query;
    import com.google.cloud.bigtable.data.v2.models.Row;
    import java.util.UUID;
    import org.springframework.web.bind.annotation.*;

    @RestController
    @RequestMapping("/sessions")
    public class SessionController {

        private final BigtableDataClient dataClient =
            BigtableDataClient.create("my-project", "my-instance");

        @GetMapping
        public Iterable<Row> sessions(@RequestParam String userId,
                                      @RequestAttribute String tenantId) {
            // Validate the user input against a strict format before use.
            UUID parsed = UUID.fromString(userId);
            String prefix = tenantId + "#" + parsed + "#";

            // Closed, deterministic key range bounded to the caller's rows.
            Query query = Query.create("sessions")
                .range(prefix, prefix.substring(0, prefix.length() - 1)
                    + (char) (prefix.charAt(prefix.length() - 1) + 1));

            return dataClient.readRows(query);
        }
    }
  ```



=== "Javascript"

  ```javascript
    const express = require('express');
    const { Bigtable } = require('@google-cloud/bigtable');
    const { validate: isUuid } = require('uuid');

    const bigtableClient = new Bigtable();
    const table = bigtableClient.instance('my-instance').table('sessions');
    const app = express();

    function validateUserId(raw) {
      if (!isUuid(raw)) {
        throw new Error('Invalid user identifier');
      }
      return raw;
    }

    app.get('/sessions', async (req, res) => {
      // tenantId comes from the authenticated session, not the request.
      const tenantId = req.session.tenantId;
      const userId = validateUserId(req.query.user_id);

      const start = `${tenantId}#${userId}#`;
      // Deterministic, closed stop key bounds the read to the caller's rows.
      const stop = start.slice(0, -1) +
        String.fromCharCode(start.charCodeAt(start.length - 1) + 1);

      const [rows] = await table.getRows({ start, end: stop });
      res.json(rows.map((row) => row.id));
    });

    app.listen(3000, () => {
      console.log('Server started on port 3000');
    });
  ```
