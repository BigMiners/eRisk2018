# erisk2018data
Contains the handler module, which parses the data for a given task  
E.g.

```python
from erisk2018data.handler import Task, batchify
task_one = Task('path/to/task1')
training_chunks, test_chunks = task_one.get_split('a')
chunk = training_chunks[0]
length_of_chunk = len(chunk) 
chunk_as_list = list(chunk)
chunk_in_batches = batchify(chunk, batch_size=64)
```

Install from GitHub

```
pip install git+https://github.com/BigMiners/eRisk2018/eRisk-2018-parser.git
```

Building the package

```
source myvirtualenv/bin/activate
cd navigate/to/erisk-2018-parser
pip install .
```
## Classes 

### Task 
    
#### Static methods

    __init__(self, path, reader=None)  
        Initialize self.  See help(type(self)) for accurate signature.
        
    text_only_xml(path)
        Retrieves the text (titles and content) from a user's writings at a given chunk. Pass this function
        as a parameter to __init__
        :param path: path to xml file
        :return: concatenated titles (from empty posts) and contents

    verbatim_xml(path)
        Retrieves the xml from a user's writings at a given chunk. Pass this function
        as a parameter to __init__
        :param path: path to xml file
        :return: xml contents as a string

    with_dates_xml(path)
        Retrieves the text (titles and content) and dates from a user's writings at a given chunk. Pass this function
        as a parameter to __init__
        :param path: path to xml file
        :return: concatenated dates, titles (from empty posts) and contents
        

#### Instance methods  

    get_split(self, name)
        Gives a list of 10 generators (1 per chunk) for a given split
        :param name: name of the split
        :return: list of train chunks, list of test chunks
