"""
This script translates JSON-LD vocabularies into N-Triples using
http://rdf-translator.appspot.com/ REST service by Alex Stolz
"""
__author__ = 'lorenzo'

import os
import pycurl
from urllib import urlencode

url = 'http://rdf-translator.appspot.com/convert/json-ld/nt/content'

def _curling(url, params, file):
    """
    POST to a remote url and print the response in a file
    :param url: target url
    :param params: parameters in the request
    :param file: name of the output file
    :return: body of the response
    """
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    # if request is GET
    #if params: c.setopt(c.URL, url + '?' + urlencode(params))

    # if request is POST
    post_data = params
    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)

    c.setopt(c.WRITEDATA, file)
    c.perform()
    c.close()

    return None


def readjson(path):
    with open(path, 'r') as f:
        content = f.read()
    return content

jsonpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ld+json')
ntpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ntriples')

ld_json = ((readjson(os.path.join(path, filename)), filename[:-5]) for path, dirs, files in os.walk(jsonpath) for filename in files if filename.endswith(".json"))

for c, f in ld_json:
    print f
    filename = f.lower()
    filename += '.ntriples'
    with open(os.path.join(ntpath, filename), 'wb+') as file:
        _curling(url, {'content': c}, file)
