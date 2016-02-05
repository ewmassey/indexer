"""This script makes the search to wikipedia by passing the search keyword as the only argument."""
import sys

from elasticsearch import Elasticsearch

import config


def title_to_url(title):
    """Takes the article title and turns it into a wikipedia URL"""
    title = title.replace(' ', '_')
    return config.WIKIPEDIA_URL + title


def search(keyword):
    """Performs the search against elasticsearch."""
    es = Elasticsearch()
    result = es.search(index=config.ELASTIC_SEARCH_INDEX, body={
        'query': {
            'multi_match': {
                'query': keyword,
                'fuzziness': 1,
                'prefix_length': 1,
                'fields': ['title^10', 'body']
            }
        }
    })

    results = []
    for hit in result['hits']['hits']:
        results.append((hit['_score'], title_to_url(hit['_source']['title'])))
    return results


def search_and_print(keyword):
    """Used for calling the search function and printing the results."""
    print "Searched for:", keyword
    for score, url in search(keyword):

        print score, url
    print


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Keyword at positional argument 1 is required."
        sys.exit(1)

    keyword = sys.argv[1]

    search_and_print(keyword)
