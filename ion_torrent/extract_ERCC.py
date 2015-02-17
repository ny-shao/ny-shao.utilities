#! /usr/bin/#!/usr/bin/env python

# Extract spik-in results from ion torrent server.
# Tested on Torrent Suite 4.4.
# Ning-Yi SHAO, CVI, Stanford.

import requests
import json
import sys

# Query list of resultName
queries = [u'Auto_snxxxx_Chip_1',
        u'Auto_snxxxx_Chip_2']

# "ERCC_Analysis", "PartekFlowUploader", "FileExporter", "coverageAnalysis"
query_plugins = [u'ERCC_Analysis']

# Query round 1. Extract the total counts of the plugins. The first query only
# return 20 elements.
ts_api_request = requests.get("http://ts_server_address/rundb/api/v1/pluginresult/",
    params={"format": "json"}, auth=('ionuser', 'ionuser'))

ts_api_response = ts_api_request.json()
total_count = ts_api_response["meta"]["total_count"]

# Query round 2. Looping to search results in the `queries`.
ts_api_request = requests.get("http://ts_server_address/rundb/api/v1/pluginresult/",
    params={"format": "json", "limit":total_count}, auth=('ionuser', 'ionuser'))

ts_api_response = ts_api_request.json()
pluginresults = ts_api_response["objects"]

for pluginresult in pluginresults:
    if pluginresult[u'resultName'] in queries:
        resultName = pluginresult[u'resultName']
        if pluginresult[u'pluginName'] in query_plugins:
            path = pluginresult[u'path'].replace("results/analysis/", "")
            for sample in pluginresult[u'store']['barcodes'].keys():
                print sample
                print("http://ts_server_address%s/%s/ercc.counts"%(path, sample))
                resp = requests.get("http://ts_server_address%s/%s/ercc.counts"%(path, sample),
                    auth=('ionuser', 'ionuser'))
                out_f = file(resultName + "_" + sample + "_ERCC_counts.txt", 'w')
                out_f.write(resp.content)
                out_f.close()
