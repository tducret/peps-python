# -*- coding: utf-8 -*-

"""Top-level package for PEPS Python."""

import requests
import time
from urllib.parse import urljoin
import json

__author__ = """Thibault Ducret"""
__email__ = 'hello@tducret.com'
__version__ = '0.0.1'

_BASE_URL = "https://peps.cnes.fr/resto/api/"

_MAX_RESULTS_PER_PEPS_REQUEST = 500

# Properties to extract from the PEPS JSON (properties field)
# "orbit_direction": "orbitDirection"
# orbit_direction is the attribute name in the Result class
# orbitDirection is the property name in PEPS JSON
_RESULT_PROPERTIES_MAPPING_DICT = {
    "title": "title",
    "acquisition_date": "startDate",
    "platform": "platform",
    "instrument": "instrument",
    "sensor_mode": "sensorMode",
    "orbit_number": "orbitNumber",
    "quicklook_url": "quicklook",
    "resource_size": "resourceSize",
    "publication_date": "published",
    "cloud_cover": "cloudCover",
    "orbit_direction": "orbitDirection",
    "ingestion_date": "dhusIngestDate",
}

# Result class attributes to return in str() function
_RESULT_ATTRIBUTES = ["id",
                      "title",
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


class Client(object):
    """Fait les requêtes avec l'API PEPS"""

    def __init__(self):
        """ Init du client """

        self.session = requests.session()
        self.headers = {
                    'Host': 'peps.cnes.fr',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; \
                        WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
                    'Accept': 'application/json, text/plain, */*',
                    }

    def _get(self, url):
        """ Requête GET """
        return self.session.get(url, headers=self.headers)

    def _rechercher_images(self, id_tuile=None, collection=None,
                           nb_resultats_max=100, page=1):
        """ Rechercher les prise de vue pour l'identifiant de tuile indiqué """

        search_url = _build_search_url(id_tuile=id_tuile,
                                       collection=collection,
                                       nb_resultats_max=nb_resultats_max,
                                       page=page)
        requete = self._get(search_url)

        if requete.status_code != 200:  # 200 = OK
            raise requests.ConnectionError
        else:
            retour = requete.text
        return retour


def _build_search_url(id_tuile=None, collection=None,
                      nb_resultats_max=100, page=1):
        """ Construit l'url de requete PEPS """
        search_url = urljoin(_BASE_URL, "collections/")

        if (collection is not None) and (collection != ""):
            search_url = urljoin(search_url, "{}/".format(collection))

        search_url = urljoin(search_url, "search.json?lang=fr&\
maxRecords={}&page={}&q=&".format(nb_resultats_max, page))

        if (id_tuile is not None) and (id_tuile != ""):
            search_url += "tileid={}".format(id_tuile)

        return search_url


class Results(object):
    """Classe des résultats"""
    def __init__(self, results_json=[]):
        self.results = []
        self.json = json.loads(results_json)
        self._get_results()

    def _get_results(self):
        for resultat_dict in self.json.get("features"):
            self.results.append(Result(resultat_dict))

    def __repr__(self):
        chaine = ""
        for resultat in self.results:
            chaine += str(resultat)
        return chaine  # json.dumps(self.results, indent=1)

    def __len__(self):
        return len(self.results)

    def __getitem__(self, key):
        """ Method to access the object as a list
        (ex : results[1]) """
        return self.results[key]


class Result(object):
    """Classe d'un résultat"""
    def __init__(self, result_dict={}):
        self.result = result_dict
        self.id = self.result["id"]

        self.properties = self.result["properties"]

        for key, value in _RESULT_PROPERTIES_MAPPING_DICT.items():
            setattr(self, key, self.properties[value])

        temp = self.properties["services"]
        self.download_url = temp["download"]["url"]

        self.geometry = self.result["geometry"]

    def __str__(self):
        str_result = ""
        for key in _RESULT_ATTRIBUTES:
            str_result += "{} : {}, ".format(key, getattr(self, key))
        return str_result

    def __repr__(self):
        return str(self)

    def __getattr__(self, attr):
        """ Méthode pour accéder à la clé d'un dictionnaire comme un
        attribut (ex : result.properties) """
        return self.result.get(attr, "")
