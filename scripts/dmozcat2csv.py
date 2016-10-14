#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import csv

import tldextract
from lxml import etree
from urlparse import urlparse

__version__ = '0.2.0'

NS = {'dmoz_rdf': 'http://dmoz.org/rdf/'}

DEF_OUT_CSV = 'output.csv'

LOG_FILE = "dmozcat2csv.log"


def setup_logger(level=logging.DEBUG):
    """ Set up logging
    """
    logging.basicConfig(level=level,
                        format='%(asctime)s  %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=LOG_FILE,
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(level)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('input', help='RDF file name (XML format)')
    parser.add_argument('-o', '--output', action='store', dest='output',
                        default=DEF_OUT_CSV, help='CSV output filename')
    parser.add_argument('--with-subdomain', action='store_true', default=False)
    parser.add_argument('--without-path', action='store_true', default=False)

    results = parser.parse_args()
    return results


def get_topic_list(external_page):
    topics = set()
    for topic in external_page.findall('dmoz_rdf:topic', NS):
        topic_text = topic.text
        topics.add(topic_text)

    return topics


if __name__ == "__main__":
    args = get_args()
    if args.verbose:
        setup_logger(logging.DEBUG)
    else:
        setup_logger(logging.INFO)

    logging.debug("input RDF file = '{0!s}'".format(args.input))

    domain_category_dict = {}
    tree = etree.parse(args.input)
    root = tree.getroot()
    for external_page in root.findall('dmoz_rdf:ExternalPage', NS):
        new_topic_set = get_topic_list(external_page)
        page_link = external_page.attrib
        url_string = page_link.get('about')
        tld = tldextract.extract(url_string)
        if args.without_path:
            o = urlparse(url_string)
            if o.path != '/':
                continue
        if args.with_subdomain and tld.subdomain != '':
            domain = '.'.join([tld.subdomain, tld.domain, tld.suffix])
        else:
            domain = tld.registered_domain
        if domain == '':
            logging.warn("Cannot extract the domain from <{0!s}>"
                         .format(url_string))
            continue
        if domain not in domain_category_dict:
            domain_category_dict[domain] = new_topic_set
        else:
            domain_category_dict[domain].update(new_topic_set)

    with open(args.output, 'wb') as f:
        writer = csv.writer(f)
        for d in domain_category_dict:
            cols = [d] + list(domain_category_dict[d])
            utf8_cols = [x.encode('utf-8') for x in cols]
            writer.writerow(utf8_cols)
