
# 4XX-Bypass

To mitigate the risk of 4xx-bypass vulnerabilities, organizations should implement proper access controls, they need to implement strict control over the format in which they receive HTTP requests, by having a robust server side logic, managing rules over the HTTP methods, headers, query parameters and paths they receive.

Here are some recommendations:
  * **HTTP methods limitations**: Limit which HTTP methods can access each of your views/resources.
  * **Query parameter sanitization**: Sanitize each request's query parameters and make sure only a limited set of parameters can have an effect on the server's logic.
  * **Header limitations**: Make sure to limit what headers can effect your code, use strict rules on what header/method combos can make changes on the servers's side, and make sure your logic does not rely on header values that can be found and on the internet (like google's User-Agent).
  * **Path parsing**: Robust path parsing with strict rules and refuse requests that don't conform to your rules.

=== "Python"
   ```python
   # allow only GET and POST methods for this route
  @app.route('/limiting_method_usage', methods=['GET', 'POST'])  
  def limiting_method_usage():
      if request.method == 'GET':
          return jsonify({"message": "This is a GET request"})
      elif request.method == 'POST':
          data = request.json
          return jsonify({"message": "This is a POST request", "data": data})
   ```
   ```python
   # only use headers you expect
   @app.route('/limiting_header_values')
  def limiting_header_values():
      expected_header = request.headers.get('Expected-Header')
      ### logic depending on the expected header
   ```
   ```python
   @app.route('/sanitize/<path:url_path>', methods=['GET'])
  def sanitize_url_path(url_path):
    sanitized_path = sanitize_path(url_path)
    '''sanitize according to you requirements,
    for example, make sure there are no characters other
    than alphanumeric characters, if that is not satisfied,
    return None, which will cause an abort'''
    if sanitized_path is None:
        abort(400, description="Invalid URL path")

    # Continue processing with the sanitized path
    return jsonify({"message": "Path is sanitized", "sanitized_path": sanitized_path}) 

   ```