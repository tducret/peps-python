#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import peps
import cProfile
import json

_KIBANA_ATTRIBUTES = ["id",
                      "title",
                      "collection",
                      "acquisition_date",
                      "platform",
                      "instrument",
                      "sensor_mode",
                      "orbit_number",
                      "resource_size",
                      "publication_date",
                      "cloud_cover",
                      "orbit_direction",
                      "ingestion_date"]


def result_to_kibana(result):
    kibana_index = {"index": {"_id": result.id}}
    kibana_dict = {}
    for key in _KIBANA_ATTRIBUTES:
        kibana_dict[key] = getattr(result, key)
    return ("{}\n{}\n".format(json.dumps(kibana_index),
                              json.dumps(kibana_dict)))


def main():
    results = peps.find_products(collection="S2ST",
                                 nb_resultats_max=500)

    with open("peps.json", "w") as f:
        for result in results:
            f.write(result_to_kibana(result))

# Puis faire l'import avec :
# curl -H 'Content-Type: application/x-ndjson' \
# -XPOST 'localhost:9200/peps/result/_bulk?pretty' \
# --data-binary @peps_full.json

#cProfile.run('main()')
main()
