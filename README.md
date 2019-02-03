# JsonXMlParser

Parser for XML and JSON files with command line interface.

## JsonXMlParser command-line arguments

```
usage: main.py [-h] [-out] link {json,xml}

positional arguments:
  link              link to input file
  {json,xml}        format of output file

optional arguments:
  -h, --help        show this help message and exit
  -out , --output   path to output file
```

## Examples

### XML to JSON without path to output file

```
python3 main.py http://ip-api.com/xml/{ip} json
```

#### output.json

```JSON
{"status": "fail", "message": "invalid query", "query": "{ip}"}
```

### JSON to XML with path to output file

```
python3 main.py http://ip-api.com/json/%7Bip%7D xml -out=out.xml
```

#### out.xml

```XML
<?xml version="1.0" encoding="UTF-8"?><query><status>fail</status><message>invalid query</message><query>{ip}</query></query>
```
