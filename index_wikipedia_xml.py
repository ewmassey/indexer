"""This script responsible for parsing the XML file containing the wikipedia data."""
import sys
import re

import xml.etree.ElementTree

from elasticsearch import Elasticsearch

es = Elasticsearch()  # TODO: Make this a generic connection. Currently assumes localhost.


def _clean_tag(tag):
    """
    Helper function to remove the mediawiki url from the front of the tag string.
    """
    cruft = '{http://www.mediawiki.org/xml/export-0.10/}'
    if tag.startswith(cruft):
        return tag[len(cruft):]


def _is_redirect(body):
    """Returns true if article is a redirect link."""
    return body.startswith('#REDIRECT')


def _parse_page(page_element):
    """
    Parses a wikipedia article and returns a dictionary with the title and body of the article.
    """
    ret = {
        'title': None,
        'body': None
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
                    ret['body'] = strip_wiki_links(child.text)

    assert ret['title'] is not None, 'title is none'
    assert ret['body'] is not None, 'body is none'
    return ret


def strip_wiki_links(text):
    """cleans up the wiki links so the phrase matching will be better."""
    pattern = re.compile(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]')
    return pattern.sub(r'\1', text)


def parse_wikipedia_dump(path):
    """Parses the Wikipedia dump at the given file path and returns a dictionary of articles to index."""
    print "Parsing Wikipedia Dump %s..." % path
    root = xml.etree.ElementTree.parse(path).getroot()
    articles = {}
    for child in root:
        if 'page' == _clean_tag(child.tag):
            article = _parse_page(child)
            if not _is_redirect(article['body']):
                articles[article['title']] = article
    return articles


def index_articles(articles):
    """Sends all articles to elasticsearch for indexing."""
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
    index_articles(articles)
