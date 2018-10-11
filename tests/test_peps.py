#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `peps` package."""

# To be tested with : python3 -m pytest -vs tests/test_peps.py

#import pytest
import peps

_BASE_URL = "https://peps.cnes.fr/resto/api/"


def test_class_Client():
    c = peps.Client()
    ret = c._get("https://peps.cnes.fr")
    assert ret.status_code == 200


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
