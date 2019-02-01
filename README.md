# Parser for XML and JSON files

Expected output:
- XML -> JSON
```JSON
{"status": "fail", "message": "invalid query", "query": "{ip}"}
```
- JSON -> XML
```XML
<?xml version="1.0" encoding="UTF-8"?><query><status>fail</status><message>invalid query</message><query>{ip}</query></query>
```