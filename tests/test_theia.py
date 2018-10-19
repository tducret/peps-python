#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `peps.theia` package."""

# To be tested with : python3 -m pytest -vs tests/test_theia.py

from peps import theia
import json

_BASE_URL = "https://theia.cnes.fr/atdistrib/resto2/api/"


def json_file_to_string(filename):
    with open(filename, 'rb') as f:
        return f.read()

_THEIA_JSON_ONE_RESULT_STR = json_file_to_string(
    'tests/theia_one_result_example.json')


# --- Results class ---
def test_class_Results():
    r = theia.Results(_THEIA_JSON_ONE_RESULT_STR)
    assert len(r) == 1
    assert r[0].id == "630e9d9c-786d-5dc0-ba49-64880db092de"


# --- Result class ---
def test_class_Result():
    json_obj = json.loads(_THEIA_JSON_ONE_RESULT_STR)
    dict_result = json_obj.get("features")[0]
    r = theia.Result(dict_result)
    print()
    print(r)
    assert r.id == "630e9d9c-786d-5dc0-ba49-64880db092de"
    assert r.title == "SENTINEL2A_20181018-105349-280_L2A_T31SBU_D"
    assert r.platform == "SENTINEL2A"
    assert r.collection == "SENTINEL2"
    assert r.acquisition_date == "2018-10-18T10:53:49Z"
    assert r.instrument == ""
    assert r.sensor_mode == ""
    assert r.absolute_orbit_number == 17351
    assert r.relative_orbit_number == 51
    assert r.production_date == "2018-10-19T03:25:21Z"
    assert r.cloud_cover == 0
    assert r.download_url == "https://theia.cnes.fr/atdistrib/resto2/\
collections/SENTINEL2/630e9d9c-786d-5dc0-ba49-64880db092de/download"
    assert r.product_type == "REFLECTANCE"
    assert r.processing_level == "LEVEL2A"
    assert r.tile_id == "31SBU"
    assert r.country == "Algérie"
    assert r.continent == "Afrique"


# --- Client class ---
def test_class_Client():
    c = theia.Client()
    ret = c._get("https://theia.cnes.fr")
    assert ret.status_code == 200


def test_find_products():
    _images_a_recuperer = 10
    c = theia.Client()
    res_json = c._find_products(id_tuile=None,
                                nb_resultats_max=_images_a_recuperer,
                                page=1)
    res = json.loads(res_json)
    resultats = res.get("features")
    assert len(resultats) == _images_a_recuperer


# --- Other functions ---
def test_build_search_url():
    print()
    # Sentinel 2 tuilé
    url = theia._build_search_url()
    print(url)
    assert url == _BASE_URL + "collections/SENTINEL2/\
search.json?lang=fr&maxRecords=100&page=1&q="

    # Tuile 31TCJ
    url = theia._build_search_url(id_tuile="31TCJ")
    print(url)
    assert url == _BASE_URL + "collections/SENTINEL2/\
search.json?lang=fr&maxRecords=100&page=1&q=&tileid=T31TCJ"

    # page 2
    url = theia._build_search_url(page=2)
    print(url)
    assert url == _BASE_URL + "collections/SENTINEL2/\
search.json?lang=fr&maxRecords=100&page=2&q="

    # 10 résultats maximum
    url = theia._build_search_url(nb_resultats_max=10)
    print(url)
    assert url == _BASE_URL + "collections/SENTINEL2/\
search.json?lang=fr&maxRecords=10&page=1&q="

    # filtrage par date
    url = theia._build_search_url(start_date="2018-10-11",
                                  end_date="2018-10-12")
    print(url)
    assert url == _BASE_URL + "collections/SENTINEL2/search.json?\
lang=fr&maxRecords=100\
&page=1&q=&startDate=2018-10-11&completionDate=2018-10-12"


def test_find_products_basic():
    _images_a_recuperer = 50
    results = theia.find_products(nb_resultats_max=_images_a_recuperer)
    assert type(results) == theia.Results
    assert len(results) == _images_a_recuperer
    for result in results:
        assert result.collection == "SENTINEL2"
    print()
    print(results)


def test_find_products_with_pagination():
    # Pour tester que la fonction peut rechercher au-delà de la 1ère page de
    # résultats, on demande le nombre max + 1
    _images_a_recuperer = theia._MAX_RESULTS_PER_THEIA_REQUEST + 1
    results = theia.find_products(nb_resultats_max=_images_a_recuperer)
    assert type(results) == theia.Results
    assert len(results) == _images_a_recuperer
    for result in results:
        assert result.collection == "SENTINEL2"


def test_find_many_products():
    _images_a_recuperer = 1000
    results = theia.find_products(nb_resultats_max=_images_a_recuperer)
    assert type(results) == theia.Results
    assert len(results) == _images_a_recuperer
    for result in results:
        assert result.collection == "SENTINEL2"


def test_find_products_for_one_specific_day():
    results = theia.find_products(start_date="2018-01-01",
                                  end_date="2018-01-02",
                                  nb_resultats_max=5)
    assert type(results) == theia.Results
    print()
    for result in results:
        print(result.acquisition_date)
        assert "2018-01-01" in result.acquisition_date
