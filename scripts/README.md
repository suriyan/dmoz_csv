DMOZ Domain categorize to CSV script
====================================

Parses Open Directory RDF Dump content (from http://rdf.dmoz.org/) and grouping the categories by domain name.

Pre-requisites
--------------
- 16GB memory computer/instance is prefered to process large RDF XML content.
- Python 2.7.x
- Install additional Python's packages 

  ```pip install -r requirements.txt```


Usage
-----

```
usage: dmozcat2csv.py [-h] [-v] [--version] [-o OUTPUT] [--with-subdomain]
                      [--without-path]
                      input

positional arguments:
  input                 RDF file name (XML format)

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
  --version             show program's version number and exit
  -o OUTPUT, --output OUTPUT
                        CSV output filename
  --with-subdomain
  --without-path
```

Example
-------

```python dmozcat2csv.py content.rdf.u8 -o output.csv```

Output format
-------------

CSV file with the following columns :-

| domain name | category1 | category2 | category3 | ... | categoryN |
| --- | --- | --- | --- | --- | --- |
