'''
Created on Apr 28, 2015

@author: prateek.jain
'''
import pickle

import tldextract

import xml.etree.ElementTree as ET


ns = {'dmoz_rdf': 'http://dmoz.org/rdf/'}

file_to_write = 'parsed.csv'
dmoz_content_file = '../content.rdf.u8'


def get_classification_list(external_page):
    empty_set = set()
    for topic in external_page.findall('dmoz_rdf:topic', ns):
        topic_text = topic.text
        if topic_text not in empty_set:
            empty_set.add(topic_text)

    return empty_set


def parse_dmoz_xml_file():
    print('Parsing DMOZ File')
    tree = ET.parse(dmoz_content_file)
    root = tree.getroot()
    url_classification_dict = {}
    for external_page in root.findall('dmoz_rdf:ExternalPage', ns):
        page_link = external_page.attrib
        url_string = page_link.get('about')
        # print url_string
        # Remove all WWW text
        url_string = url_string.replace('www.', '')
        url_string = url_string.replace('WWW.', '')
        url_string = url_string.replace('http://', '')
        url_string = url_string.replace('https://', '')
        if url_string[-1:] == '/':
            url_string = url_string[:-1]

        new_topic_set = get_classification_list(external_page)

        hostname = ''

        if url_string in url_classification_dict:
            classification_set = url_classification_dict[url_string]
            classification_set = classification_set.union(new_topic_set)
        else:
            classification_set = new_topic_set
            extracted = tldextract.extract(url_string)
            try:
                hostname = "{}.{}".format(extracted.domain, extracted.suffix)
            except Exception as e:
                print(e, extracted.domain, extracted.suffix)
                domain = extracted.domain.encode('utf8', 'ignore')
                suffix = extracted.suffix.encode('utf8', 'ignore')
                hostname = "{}.{}".format(domain, suffix)

#         if hostname in url_classification_dict:
#             classification_set = url_classification_dict[hostname]
#             classification_set = classification_set.union(new_topic_set)
#
#
#         print hostname
#         print url_string
#         print str(classification_set)
        url_classification_dict[hostname] = classification_set
        url_classification_dict[url_string] = classification_set
    #if len(url_classification_dict) == 100:
    write_to_csv_file(url_classification_dict)
    # FIXME: it take >16GB disk space
    # pickle.dump(url_classification_dict, open( "dmoz_dict.p", "wb" ) )
    return url_classification_dict


def write_to_csv_file(dmoz_dictionary):
    count = 0
    try:
        dmoz_csv_file_object = open(file_to_write, 'w')
        for webpage in dmoz_dictionary:
            write_string = '"' + webpage + '",'
            classification_set = dmoz_dictionary[webpage]
            for topic in classification_set:
                write_string = write_string + '"' + topic + '",'
            write_string = write_string[:-1] + '\n'
            # print write_string
            dmoz_csv_file_object.write(write_string.encode('utf8', 'ignore'))
            count += 1
        dmoz_csv_file_object.flush()
        dmoz_csv_file_object.close()
    except Exception as e:
        print(e)
    print("Total: {}".format(count))

 
if __name__=='__main__':
    parse_dmoz_xml_file()
