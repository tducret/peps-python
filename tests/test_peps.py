#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `peps` package."""

# To be tested with : python3 -m pytest -vs tests/test_peps.py

#import pytest
import peps


def test_class_Client():
    c = peps.Client()
    ret = c._get("http://www.example.org")
    assert ret.status_code == 200


def _build_search_url():
    url = peps._build_search_url(id_tuile=None, collection="S2ST",
                                 nb_resultats_max=50, page=1)
    assert url == "https://peps.cnes.fr/resto/api/collections/S2ST/\
search.json?lang=fr&maxRecords=50&page=1&platform=S2A&q=&"
