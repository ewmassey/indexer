"""This script responsible for parsing the XML file containing the wikipedia data."""
import sys
import re

from pprint import pprint

import xml.etree.ElementTree

from elasticsearch import Elasticsearch

es = Elasticsearch()


def _clean_tag(tag):
    """
    Helper function to remove the mediawiki url from the front of the tag string.
    """
    cruft = '{http://www.mediawiki.org/xml/export-0.10/}'
    if tag.startswith(cruft):
        return tag[len(cruft):]


def _parse_page(page_element):
    """
    Parses a wikipedia article and returns a dictionary with the title and body of the article.
    """
    ret = {
        'title': None,
        'body': None,
        'redirect_to': None,
        'redirect_from': []
    }
    # Pull data from XML
    for element in page_element:
        tag = _clean_tag(element.tag)
        if tag == 'title':
            ret['title'] = element.text
        elif tag == 'revision':
            # Find the body of the article
            for child in element:
                rev_tag = _clean_tag(child.tag)
                if rev_tag == 'text':
                    ret['body'] = child.text
    assert ret['title'] is not None, 'title is none'
    assert ret['body'] is not None, 'body is none'

    # Process the Body.

    ret['body'] = wiki_to_plaintext(ret['body'])

    if 'REDIRECT' in ret['body']:

        link_match = re.match("#REDIRECT.*\[\[(.*)\]\]?.*", ret['body'])
        if link_match:
            ret['redirect_to'] = link_match.group(1)
    return ret


def wiki_to_plaintext(text):
    """cleans up the wiki markup and converts it to plaintext."""
    # TODO: Strip out Wiki Markup here.

    return text


def parse_wikipedia_dump(path):
    """Parses the Wikipedia dump at the given file path and returns a dictionary of articles to index."""
    print "Parsing Wikipedia Dump %s..." % path
    root = xml.etree.ElementTree.parse(path).getroot()
    articles = {}
    for child in root:
        if 'page' == _clean_tag(child.tag):
            article = _parse_page(child)
            articles[article['title']] = article
    return articles


def update_source_redirects(articles):

    for key in articles.keys():
        article = articles[key]  # Do this so we can delete the redirecting articles and not index them.
        destination_name = article['redirect_to']
        if destination_name is not None and destination_name in articles.keys():
            # This doesn't look like the complete set of Wikipedia articles so if the redirect might not be present.
            dest_article = articles[destination_name]
            dest_article['redirect_from'].append(key)
            del articles[key]  # Remove the article that is redirected from.


def index_articles(articles):

    print "Indexing the articles in elasticsearch."
    for i, article in enumerate(articles.values()):
        id = i + 1
        es.index(index='wikipedia', doc_type='article', id=id, body=article)
    print "%d articles were indexed." % len(articles)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "A path to the filename at positional argument 1 is required."
        sys.exit(1)

    dump_path = sys.argv[1]  # Path to the wikipedia dump.

    articles = parse_wikipedia_dump(dump_path)
    update_source_redirects(articles)

    index_articles(articles)

    #
    # pprint(articles)
