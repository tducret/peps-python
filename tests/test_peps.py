#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `peps` package."""

# To be tested with : python3 -m pytest -vs tests/test_peps.py

import peps
import json

_BASE_URL = "https://peps.cnes.fr/resto/api/"


def json_file_to_string(filename):
    with open(filename) as f:
        return f.read()

_PEPS_JSON_ONE_RESULT_STR = json_file_to_string(
    'tests/peps_one_result_example.json')


# --- Result class ---
def test_class_Result():
    json_obj = json.loads(_PEPS_JSON_ONE_RESULT_STR)
    dict_result = json_obj.get("features")[0]
    r = peps.Result(dict_result)
    print()
    print(r)
    assert r.id == "05959e39-ce82-5b39-9a30-e67ea0417204"
    assert r.title == \
        "S2A_MSIL1C_20181011T055751_N0206_R091_T43UGS_20181011T072546"
    assert r.platform == "S2A"
    assert r.acquisition_date == "2018-10-11T05:57:51.024Z"
    assert r.instrument == "MSI"
    assert r.sensor_mode == "INS-NOBS"
    assert r.orbit_number == 17248
    assert r.resource_size == 128062896
    assert r.publication_date == "2018-10-11T09:51:25.135Z"
    assert r.cloud_cover == 3.4153
    assert r.orbit_direction == "descending"
    assert r.ingestion_date == "2018-10-11T09:47:28.990Z"


# --- Client class ---
def test_class_Client():
    c = peps.Client()
    ret = c._get("https://peps.cnes.fr")
    assert ret.status_code == 200


def test_rechercher_images():
    _images_a_recuperer = 10
    c = peps.Client()
    res_json = c._rechercher_images(id_tuile=None, collection=None,
                                    nb_resultats_max=_images_a_recuperer,
                                    page=1)
    res = json.loads(res_json)
    resultats = res.get("features")
    assert len(resultats) == _images_a_recuperer


# --- Other functions ---
def test_build_search_url():
    print()
    # Sentinel 2 tuilé
    url = peps._build_search_url(collection="S2ST")
    print(url)
    assert url == _BASE_URL + "collections/S2ST/\
search.json?lang=fr&maxRecords=100&page=1&q=&"

    # Tous sentinels confondus, tuile 31TCJ
    url = peps._build_search_url(id_tuile="31TCJ")
    print(url)
    assert url == _BASE_URL + "collections/\
search.json?lang=fr&maxRecords=100&page=1&q=&tileid=31TCJ"

    # Tuile 31TCJ
    url = peps._build_search_url(id_tuile="31TCJ")
    print(url)
    assert url == _BASE_URL + "collections/\
search.json?lang=fr&maxRecords=100&page=1&q=&tileid=31TCJ"

    # page 2
    url = peps._build_search_url(page=2)
    print(url)
    assert url == _BASE_URL + "collections/\
search.json?lang=fr&maxRecords=100&page=2&q=&"

    # 10 résultats maximum
    url = peps._build_search_url(nb_resultats_max=10)
    print(url)
    assert url == _BASE_URL + "collections/\
search.json?lang=fr&maxRecords=10&page=1&q=&"
