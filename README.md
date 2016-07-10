# py-quick-crawlers

Exposes a set of Python based APIs wrapping a collection of Scrapy based generic crawlers, for quick use, hiding out all the complex crawling configurations and coding complexities.

## Installation

This package is not in PyPi yet. For now, download / install directly from GitHub.
```
sudo pip install git+https://github.com/vdraceil/py-quick-crawlers.git
```

## API

APIs are exposed via the Controller module.
```python
from py_quick_crawlers import Controller

# you can invoke the APIs on the Controller instance
controller = Controller()
```

See `examples/` for detailed usage instructions.

#### Pattern Match Crawl

Crawls a given set of URLs for a given depth and retrieves all items that matches the given set of patterns.

###### Signature
```python
pattern_match_crawl(target, patter_dict, out_file=None, feed_type='JSON')
```

###### Parameters
__target__ - A list of tuples specifying the start URLs and individual depths `[ (<START_URL1>, <DEPTH1>), (<START_URL2>, <DEPTH2>), ... ]`  
__pattern_dict__ - A dictionary mapping names (for output formatting) to patterns as compiled regular expressions `{ '<key1>': <REGEX1>, 'key2': <REGEX2>, ... }`  
__out_file__ - Output file; replaced if it exists  
__feed_type__ - Output file format `'<JSON/CSV/XML>'`

###### Output
A file with the crawled data in the requested feed format.

#### Content Download Crawl

Crawls a given set of URLs for a given depth and downloads all files matching the given list of file patterns into a output directory.

###### Signature
```python
content_download_crawl(target, pattern_list, out_dir=None, enable_dir_structure=False)
```

###### Parameters
__target__ - A list of tuples specifying the start URLs and individual depths `[ (<START_URL1>, <DEPTH1>), (<START_URL2>, <DEPTH2>), ... ]`  
__pattern_list__ - A list of allowed file patterns as compiled regular expressions `[ <REGEX1>, <REGEX2>, ... ]`  
__out_dir__ - Output directory; created if it does not exist  
__enable_dir_structure__ - Boolean `<True/False>`  
Determines how the files are downloaded in the output directory.  
If `True`, the downloaded files will be organized in a directory structure resembling its URL in the web server.  
If `False`, the all downloaded files will be at the first level in the output directory with their names being SHA1 hashes of their URL path.

###### Output
A directory of files downloaded from target websites matching the given file patterns.
