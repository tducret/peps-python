#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import peps
import json
from datetime import datetime, timedelta

#_START_DATE = "2014-06-14"  # First Sentinel Sat data on 15/06/2014
_START_DATE = "2018-10-01"
_END_DATE = datetime.today().strftime("%Y-%m-%d")

_KIBANA_ATTRIBUTES = peps._RESULT_ATTRIBUTES


def result_to_kibana(result):
    kibana_index = {"index": {"_id": result.id}}
    kibana_dict = {}
    for key in _KIBANA_ATTRIBUTES:
        kibana_dict[key] = getattr(result, key)
    return ("{}\n{}\n".format(json.dumps(kibana_index),
                              json.dumps(kibana_dict)))


def main():

    start = datetime.strptime(_START_DATE, "%Y-%m-%d")
    end = datetime.strptime(_END_DATE, "%Y-%m-%d")

    while start < end:
        day_str = start.strftime("%Y-%m-%d")

        print("Search products for {}".format(day_str))

        results = peps.find_products(
            start_date=day_str+"T00:00:00",
            end_date=day_str+"T23:59:59",
            nb_resultats_max=100000)

        print("{} results for {}".format(len(results),
                                         day_str))

        if len(results) > 0:
            filename = "peps_{}.json".format(day_str)
            with open(filename, "w") as f:
                for result in results:
                    f.write(result_to_kibana(result))

        start = start + timedelta(days=1)  # increase day one by one

# Puis faire l'import avec :
# curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/peps/result/_bulk?pretty' --data-binary @peps_full.json

# voire
# for file in *
# do
#   curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/peps/result/_bulk?pretty' --data-binary @$file
# done

main()
