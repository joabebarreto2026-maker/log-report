There is an Apache-style access log at /app/access.log in the working directory. Parse it
and write a JSON summary report to /app/report.json (absolute path).

The report must be a single JSON object with exactly these three keys:

- total_requests: an integer, the total number of log lines (requests) in the file.
- unique_ips: an integer, the number of distinct client IP addresses (the first field of
  each log line) that appear in the file.
- top_path: a string, the request path (e.g. "/index.html") that occurs most often across
  all requests, taken from the quoted request line.

Success criteria:

1. /app/report.json exists and contains a single valid JSON object.
2. That object has exactly the keys total_requests, unique_ips, and top_path, and no others.
3. total_requests equals the number of non-empty lines in /app/access.log.
4. unique_ips equals the number of distinct IP addresses across those lines.
5. top_path equals the single most frequently requested path in the log.
