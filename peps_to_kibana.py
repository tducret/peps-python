#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import peps
import json

_KIBANA_ATTRIBUTES = peps._RESULT_ATTRIBUTES


def result_to_kibana(result):
    kibana_index = {"index": {"_id": result.id}}
    kibana_dict = {}
    for key in _KIBANA_ATTRIBUTES:
        kibana_dict[key] = getattr(result, key)
    return ("{}\n{}\n".format(json.dumps(kibana_index),
                              json.dumps(kibana_dict)))


def main():
    results = peps.find_products(start_date="2018-10-10T00:00:00",
                                 end_date="2018-10-10T01:59:59",
                                 nb_resultats_max=100000)
    print("{} results".format(len(results)))

    with open("peps.json", "w") as f:
        for result in results:
            f.write(result_to_kibana(result))

# Puis faire l'import avec :
# curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/peps/result/_bulk?pretty' --data-binary @peps_full.json

main()
