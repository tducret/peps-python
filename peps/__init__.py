# -*- coding: utf-8 -*-

"""Top-level package for PEPS Python."""

import requests
import time
from urllib.parse import urljoin

__author__ = """Thibault Ducret"""
__email__ = 'hello@tducret.com'
__version__ = '0.0.1'

_BASE_URL = "https://peps.cnes.fr/resto/api/"

_NB_MAX_RESULTATS_REQUETE_PEPS = 500
_MAX_REQUEST_TRIALS = 5


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
maxRecords={}&page={}&q=".format(nb_resultats_max, page))

        if (id_tuile is not None) and (id_tuile != ""):
            search_url += "&tileid={}".format(id_tuile)

        print(search_url)
        return search_url
