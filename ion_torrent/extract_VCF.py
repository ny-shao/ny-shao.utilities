#! /usr/bin/#!/usr/bin/env python

# Extract spik-in results from ion torrent server.
# Tested on Torrent Suite 4.4.
# Ning-Yi SHAO, CVI, Stanford.

import requests
import json
import sys

def download_file(url, resultName, sample):
    ## Modified from:
    ## http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
    local_filename = "_".join([resultName, sample, url.split('/')[-1]])
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True, auth=('ionuser', 'ionuser'))
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename

ts_server_add = "127.0.0.1" # address of Ion Torrent Server

# Query list of resultName
queries = [u'xxx_001',
        u'xxx_002']

# "ERCC_Analysis", "PartekFlowUploader", "FileExporter", "coverageAnalysis"
query_plugins = [u'variantCaller']

# Query round 1. Extract the total counts of the plugins. The first query only
# return 20 elements.
ts_api_request = requests.get("http://%s/rundb/api/v1/pluginresult/"%(ts_server_add,),
    params={"format": "json"}, auth=('ionuser', 'ionuser'))

ts_api_response = ts_api_request.json()
total_count = ts_api_response["meta"]["total_count"]

# Query round 2. Looping to search results in the `queries`.
ts_api_request = requests.get("http://%s/rundb/api/v1/pluginresult/"%(ts_server_add,),
    params={"format": "json", "limit":total_count}, auth=('ionuser', 'ionuser'))

ts_api_response = ts_api_request.json()
pluginresults = ts_api_response["objects"]

for pluginresult in pluginresults:
    if pluginresult[u'resultName'] in queries:
        resultName = pluginresult[u'resultName']
        print(resultName)
        if pluginresult[u'pluginName'] in query_plugins:
            path = pluginresult[u'path'].replace("results/analysis/", "")
            for sample in pluginresult[u'store']['barcodes'].keys():
                for file in pluginresult[u'store'][u'files']:
                    path = file['server_path'].replace("results/analysis/", "")
                    url = "http://%s%s"%(ts_server_add, path)
                    print(download_file(url, resultName, sample))
