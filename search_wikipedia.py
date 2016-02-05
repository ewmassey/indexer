import sys

from elasticsearch import Elasticsearch

WIKIPEDIA_URL = 'https://en.wikipedia.org/wiki/'


def title_to_url(title):

    title = title.replace(' ', '_')
    return WIKIPEDIA_URL + title

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "A path to the filename at positional argument 1 is required."
        sys.exit(1)

    keyword = sys.argv[1]

    es = Elasticsearch()

    result = es.search(index='wikipedia', body={
        'query': {
            'match': {
                'title': {
                    'query': keyword,
                    'fuzziness': 2,
                    'prefix_length': 1
                }
            }
        }
    })

    for hit in result['hits']['hits']:
        print hit['_score'], title_to_url(hit['_source']['title'])

    # Total number of hits
    # link to the page...how do i get this?
    # relevance