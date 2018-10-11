#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import peps
import cProfile


def main():
    results = peps.find_products(collection="S2ST",
                                 nb_resultats_max=500)

    with open("peps.json", "w") as f:
        f.write(str(results))

# Puis faire l'import avec :
# curl -H 'Content-Type: application/x-ndjson' \
# -XPOST 'localhost:9200/peps/result/_bulk?pretty' \
# --data-binary @peps_full.json

cProfile.run('main()')
