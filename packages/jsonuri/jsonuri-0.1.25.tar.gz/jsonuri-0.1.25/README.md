
JSONURI-PY
==============
 
This package helps you convert Python dictionaries into an HTTP GET request parameters, and vice-versa. 

An example of a practical application would be to send JSON data over HTTP GET, e.g. to a static resource small.png, and harvest the data from access logs instead of running real-time data collection.

**Note**: You should avoid send sensitive information using this mechanism, or at least ensure you send your data over SSL.

Equivalent libs/packages:
==========================

| Language | Repo                                |
|----------|-------------------------------------|
| JavaScript   | https://github.com/guidj/jsonuri-js |


Examples:
=============

Serialization:
---------------

```python
>>> import json
>>> import urllib.parse
>>> from jsonuri import jsonuri
>>> jsonuri.serialize(json.loads('{"age": "31", "name": "John", "account": {"id": 127, "regions": ["US", "SG"]}}'))
'account%3Aregions%5B0%5D%3DUS%26account%3Aregions%5B1%5D%3DSG%26account%3Aid%3D127&age%3D31&name%3DJohn'
>>> jsonuri.serialize(json.loads('{"age": "31", "name": "John", "account": {"id": 127, "regions": ["US", "SG"]}}'), encode=False)
'account:regions[0]=US&account:regions[1]=SG&account:id=127&age=31&name=John'
```

Desirialization
----------------

```python
>>> string = "account:regions[0]=US&account:regions[1]=SG&account:id=127&age=31&name=John"
>>> jsonuri.deserialize(string)
{'account': {'regions': ['US', 'SG'], 'id': '127'}, 'age': '31', 'name': 'John'}
```

Notes
======

The package was not designed to process HTML form data, specifically multi-value variables, i.e. from select attributes. Though if you convert the data to a JSON/JavaScript object, that should work.
