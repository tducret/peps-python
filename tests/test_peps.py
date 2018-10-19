#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `peps` package."""

# To be tested with : python3 -m pytest -vs tests/test_peps.py

import peps
import json

_BASE_URL = "https://peps.cnes.fr/resto/api/"


def json_file_to_string(filename):
    with open(filename, 'rb') as f:
        return f.read()

_PEPS_JSON_ONE_RESULT_STR = json_file_to_string(
    'tests/peps_one_result_example.json')


# --- Results class ---
def test_class_Results():
    r = peps.Results(_PEPS_JSON_ONE_RESULT_STR)
    assert len(r) == 1
    assert r[0].id == "05959e39-ce82-5b39-9a30-e67ea0417204"


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
    assert r.collection == "S2ST"
    assert r.acquisition_date == "2018-10-11T05:57:51.024Z"
    assert r.instrument == "MSI"
    assert r.sensor_mode == "INS-NOBS"
    assert r.absolute_orbit_number == 17248
    assert r.relative_orbit_number == 91
    assert r.resource_size == 128062896
    assert r.publication_date == "2018-10-11T09:51:25.135Z"
    assert r.cloud_cover == 3.4153
    assert r.orbit_direction == "descending"
    assert r.ingestion_date == "2018-10-11T09:47:28.990Z"
    assert r.download_url == "https://peps.cnes.fr/resto/collections/S2ST/\
05959e39-ce82-5b39-9a30-e67ea0417204/download"
    assert r.product_type == "S2MSI1C"
    assert r.processing_level == "LEVEL1C"
    assert r.storage_mode == "disk"
    assert r.tile_id == "43UGS"
    assert r.country == "Kazakhstan"
    assert r.continent == "Asie"


# --- Client class ---
def test_class_Client():
    c = peps.Client()
    ret = c._get("https://peps.cnes.fr")
    assert ret.status_code == 200


def test_find_products():
    _images_a_recuperer = 10
    c = peps.Client()
    res_json = c._find_products(id_tuile=None, collection=None,
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
search.json?lang=fr&maxRecords=100&page=1&q="

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
search.json?lang=fr&maxRecords=100&page=2&q="

    # 10 résultats maximum
    url = peps._build_search_url(nb_resultats_max=10)
    print(url)
    assert url == _BASE_URL + "collections/\
search.json?lang=fr&maxRecords=10&page=1&q="

    # filtrage par date
    url = peps._build_search_url(start_date="2018-10-11T14:04:00",
                                 end_date="2018-10-12T14:05:00")
    print(url)
    assert url == _BASE_URL + "collections/search.json?lang=fr&maxRecords=100\
&page=1&q=&startDate=2018-10-11T14:04:00&completionDate=2018-10-12T14:05:00"


def test_find_products_basic():
    _images_a_recuperer = 50
    results = peps.find_products(collection="S3",
                                 nb_resultats_max=_images_a_recuperer)
    assert type(results) == peps.Results
    assert len(results) == _images_a_recuperer
    for result in results:
        assert result.collection == "S3"
    print()
    print(results)


def test_find_products_with_pagination():
    # Pour tester que la fonction peut rechercher au-delà de la 1ère page de
    # résultats, on demande le nombre max + 1
    _images_a_recuperer = peps._MAX_RESULTS_PER_PEPS_REQUEST + 1
    results = peps.find_products(collection="S2ST",
                                 nb_resultats_max=_images_a_recuperer)
    assert type(results) == peps.Results
    assert len(results) == _images_a_recuperer
    for result in results:
        assert result.collection == "S2ST"


def test_find_many_products():
    _images_a_recuperer = 1000
    results = peps.find_products(collection="S2ST",
                                 nb_resultats_max=_images_a_recuperer)
    assert type(results) == peps.Results
    assert len(results) == _images_a_recuperer
    for result in results:
        assert result.collection == "S2ST"


def test_find_products_for_one_specific_hour():
    results = peps.find_products(start_date="2018-01-01T00:00:00",
                                 end_date="2018-01-01T00:59:59",
                                 nb_resultats_max=5)
    assert type(results) == peps.Results
    print()
    for result in results:
        print(result.acquisition_date)
        assert "2018-01-01T00:" in result.acquisition_date


def test_get_tile_id_from_title():
    assert peps._get_tile_id_from_title("NOT_A_GOOD_TITLE") == ""
    assert peps._get_tile_id_from_title("S2A_WRONG") == ""
    assert peps._get_tile_id_from_title(
        "S2B_MSIL1C_20181012T025639_N0206_R032_T50TNQ_20181012T054303") == \
        "50TNQ"
