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
_MAX_REQUEST_TRIALS = 10  # Maximum number of request trials

# Properties to extract from the PEPS JSON (properties field)
# "orbit_direction": "orbitDirection"
# orbit_direction is the attribute name in the Result class
# orbitDirection is the property name in PEPS JSON
_RESULT_PROPERTIES_MAPPING_DICT = {
    "title": "title",
    "collection": "collection",
    "acquisition_date": "startDate",
    "platform": "platform",
    "instrument": "instrument",
    "sensor_mode": "sensorMode",
    "absolute_orbit_number": "orbitNumber",
    "relative_orbit_number": "relativeOrbitNumber",
    "orbit_direction": "orbitDirection",
    "quicklook_url": "quicklook",
    "resource_size": "resourceSize",
    "publication_date": "published",
    "cloud_cover": "cloudCover",
    "ingestion_date": "dhusIngestDate",
    "product_type": "productType",
    "processing_level": "processingLevel",
    "snow_cover": "snowCover",
    "tile_id": "mgrs",
}

# Result class attributes to return in str() function
_RESULT_ATTRIBUTES = ["id",
                      "title",
                      "collection",
                      "acquisition_date",
                      "platform",
                      "instrument",
                      "sensor_mode",
                      "absolute_orbit_number",
                      "relative_orbit_number",
                      "orbit_direction",
                      "resource_size",
                      "publication_date",
                      "cloud_cover",
                      "ingestion_date",
                      "product_type",
                      "processing_level",
                      "snow_cover",
                      "storage_mode",
                      "tile_id",
                      "country",
                      "continent"]


# --- Client class ---
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

    def _get_with_retry(self, url):
        """ GET request with retry if a connection error happens """
        trials = 0
        while trials < _MAX_REQUEST_TRIALS:
            try:
                trials += 1
                ret = self._get(url)
            except requests.exceptions.ConnectionError:
                print("ConnectionError : {}".format(trials))
                time.sleep(10)
                pass
        return ret

    def _find_products(self, id_tuile=None, collection=None,
                       nb_resultats_max=100, page=1):
        """ Rechercher les prise de vue pour l'identifiant de tuile indiqué """

        search_url = _build_search_url(id_tuile=id_tuile,
                                       collection=collection,
                                       nb_resultats_max=nb_resultats_max,
                                       page=page)
        requete = self._get_with_retry(search_url)

        retour = requete.text
        return retour


# --- Results class ---
class Results(object):
    """Classe des résultats"""
    def __init__(self, results_json=[]):
        self.results = []
        if results_json != []:
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

    def __getattr__(self, method):
        return getattr(self.results, method)

    def __str__(self):
        s = ""
        for r in self.results:
            s += str(r) + "\n"
        return s


# --- Result class ---
class Result(object):
    """Classe d'un résultat"""
    def __init__(self, result_dict={}):
        self.result = result_dict
        self.id = self.result["id"]

        self.properties = self.result["properties"]

        for key, value in _RESULT_PROPERTIES_MAPPING_DICT.items():
            setattr(self, key, self.properties.get(value, ""))

        temp = self.properties["services"]
        self.download_url = temp["download"]["url"]

        self.geometry = self.result["geometry"]

        self.storage_mode = self.properties["storage"]["mode"]

        self.country = self._get_country(self.properties["keywords"])
        self.continent = self._get_continent(self.properties["keywords"])

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

    def _get_keyword_value(self, keywords, keyword_type):
        keyword_value = ""
        for key, value in keywords.items():
            if value.get("type", "") == keyword_type:
                keyword_value = value.get("name")
                break
        return keyword_value

    def _get_country(self, keywords):
        return self._get_keyword_value(keywords, keyword_type="country")

    def _get_continent(self, keywords):
        return self._get_keyword_value(keywords, keyword_type="continent")


# --- Other functions ---
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


def find_products(id_tuile=None, collection=None, nb_resultats_max=100):
    """ Rechercher les prise de vue sur PEPS
    (avec gestion de la pagination) """
    peps = Client()
    liste_resultats = Results()

    # On tronque le nombre de résultats max par requête au maximum
    # supporté par PEPS
    if nb_resultats_max > _MAX_RESULTS_PER_PEPS_REQUEST:
        nb_resultats_max_requete = _MAX_RESULTS_PER_PEPS_REQUEST
    else:
        nb_resultats_max_requete = nb_resultats_max

    page = 1
    while True:
        # Combien restent-ils de produit à rechercher?
        # Ex :
        # 1er passage dans la boucle : nb_resultats_restants = 501 - 0
        # 2ème passage : nb_resultats_restants = 501 - 500
        nb_resultats_restants = nb_resultats_max - len(liste_resultats)
        # S'il en reste moins que le nombre max par requête
        # 1er passage dans la boucle : 501 > 500
        # 2ème passage dans la boucle : 1 < 500 => On ne demandera donc qu'un
        # résultat dans la 2ème requête
        if nb_resultats_restants < nb_resultats_max_requete:
            nb_resultats_max_requete = nb_resultats_restants
        resultats_json = peps._find_products(
            id_tuile=id_tuile,
            collection=collection,
            nb_resultats_max=nb_resultats_max_requete, page=page)

        resultats = Results(resultats_json)

        liste_resultats.extend(resultats)

        if len(liste_resultats) >= nb_resultats_max:
            # Nous avons le nombre de résultats demandé
            break
        elif len(resultats) == 0:
            # Nous sommes arrivés au bout des résultats
            break
        else:
            page += 1

    return liste_resultats
