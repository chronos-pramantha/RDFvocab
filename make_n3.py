"""
This script translates JSON-LD vocabularies into N-Triples using
http://rdf-translator.appspot.com/ REST service by Alex Stolz
"""
__author__ = 'lorenzo'

import os
import pycurl
from urllib import urlencode


def _curling(url, params, file):
    """
    GET to a remote url and print the response in a file
    :param url: target url
    :param params: parameters in the request
    :param file: path of the output file
    :return: body of the response
    """
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    if params: c.setopt(c.URL, url + '?' + urlencode(params))

    # if request is POST
    #post_data = params
    # Form data must be provided already urlencoded.
    #postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    #c.setopt(c.POSTFIELDS, postfields)

    c.setopt(c.WRITEDATA, file)
    c.perform()
    c.close()

    return None

jsonpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ld+json')
ntpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ntriples')

ld_json = (filename[:-5] for path, dirs, files in os.walk(jsonpath) for filename in files if filename.endswith(".json"))

for f in ld_json:
    filename = f.lower()
    print filename
    url = 'http://rdf-translator.appspot.com/convert/json-ld/nt/http%3A%2F%2Fontology.projectchronos.eu%2F' + filename +'%2F%3Fformat%3Djsonld'
    filename += '.ntriples'
    with open(os.path.join(ntpath, filename), 'wb+') as file:
        _curling(url, {}, file)
