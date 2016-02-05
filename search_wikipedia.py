from elasticsearch import Elasticsearch

from pprint import pprint

es = Elasticsearch()

result = es.search(index='wikipedia', body={'query': {'match': {'title': 'Apple'}}})

pprint(result)
