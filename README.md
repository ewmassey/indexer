Wikipedia Indexer
=================

The wikipedia indexer takes an xml dump from wikipedia and indexes each article in an instance of elastic search.

### Indexing the Articles

Install elasticsearch for your system per the instructions on their website: https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html

Install the required python libs via
```
pip install -r requirements.txt
```

Run Elasticsearch from via in the folder where it was installed:
```
./bin/elasticsearch
```

Run the indexer script where "articles.xml" is the path to the wikipedia xml dump.
```
python index_wikipedia_xml.py articles.xml
```
At this point you are ready to perform searches.

### Searching the Wikipedia dump
If the above steps went well searching is as simple as:
```
python search_wikipedia.py 'Great Alexander'
```
Output:
```
Searched for: Great Alexander
4.4585247 https://en.wikipedia.org/wiki/Alexander_the_Great
2.9235675 https://en.wikipedia.org/wiki/Alexander
1.8272297 https://en.wikipedia.org/wiki/Alexander_Balas
1.8272297 https://en.wikipedia.org/wiki/Alexander_Jagiellon
1.8272297 https://en.wikipedia.org/wiki/Alexander_Kerensky
1.8272297 https://en.wikipedia.org/wiki/Alexander_technique
1.4617838 https://en.wikipedia.org/wiki/Alexander_Graham_Bell
1.4617838 https://en.wikipedia.org/wiki/Alexander_III_of_Russia
1.3924997 https://en.wikipedia.org/wiki/Anthony_the_Great
1.357819 https://en.wikipedia.org/wiki/Severus_Alexander

```

To Run all the search cases mentioned in the PDF:

```
python run_search_cases.py
```