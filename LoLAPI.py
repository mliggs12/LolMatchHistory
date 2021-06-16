"""@package LoLAPI
    A Python class that allows access to some of the functionality in the
    Riot Games API for League of Legends (LoL).

    This package attempts to stay on top of changes to the API and allow an
    easy to use interface with the LoL API.
"""
import logging
import requests

API_KEY = 'RGAPI-d5ba2836-6f7a-4ed3-af0f-bd8404bbdb52'
BASE_URL = 'https://americas.api.riotgames.com/lol/'    # only V5?
# Liggs
PUUID = 'KcjCE8Bq5WQvq988sErZaNMKJNEIqYOvPLMG_WOc-A4Jb0xcrRLCGvEsbfNkjNADjohYl1PO9f-trg'


class LoLAPI:
    """The LoLAPI class providing blackbox use of the League of Legends (LoL)
    API by Riot Games.

    This is the main class of the API module. This should be the only class
    used in applications built around the API. The LoLAPI class allows access
    to the GET requests supported by the LoL API.

    Missing Functionality:
    """

    def __init__(self, api_key, debug=False):
        self.api_key = api_key
        self.DEBUG = debug

        if debug:
            logging.basicConfig(
                filemode='w',
                format='%(asctime)s - %(name)s - %(levelname)s:\n%(message)s',
                level=logging.DEBUG
            )

    def execute(self, url=None, method='GET', params=None, headers=None):
        """Bootstraps and executes the request."""
        method = method.lower()
        headers = {'X-Riot-Token': self.api_key}
        # Executes the request
        if method == "get" or 'method' not in locals():
            r = requests.get(url, json=params, headers=headers)
        elif method == "post":
            r = requests.post(url, json=params, headers=headers)
        else:
            return None
        # Log response content
        logging.debug("Response Content: %s" % r.text)

        return r.json()

    # --------------------
    # MATCH-V5 API Methods
    # --------------------

    def matchlist_by_puuid(self, puuid, start=None, count=None):
        """Get a list of match ids by puuid

            :param puuid: str
            :param start: int - Start index. Defaults to 0.
            :param count: int - Match id count. Defaults to 20. Valid values: 0 to 100.

            :returns: List[match_id: str]
        """
        endpoint = BASE_URL + f'match/v5/matches/by-puuid/{puuid}/ids'
        # Working with optional parameters in endpoint URL
        if start and count:
            endpoint += f'?start={start}&count={count}'
        elif start:
            endpoint += f'?start={start}'
        elif count:
            endpoint += f'?count={count}'

        return self.execute(endpoint)

    def match_by_id(self, match_id):
        """Get a match by match id

            :param match_id: str

            :returns: MatchDto
        """
        endpoint = BASE_URL + f'match/v5/matches/{match_id}'

        return self.execute(endpoint)

    def match_timeline_by_id(self, match_id):
        """Get a match timeline by match id

            :param match_id: str
            :returns: MatchTimelineDto
        """
        endpoint = BASE_URL + f'match/v5/matches/{match_id}/timeline'

        return self.execute(endpoint)


lol = LoLAPI(API_KEY, True)
m_id = "NA1_3934251577"
# lol.match_timeline_by_id(m_id)
# lol.matchlist_by_puuid(PUUID, count=100)
lol.match_by_id(m_id)
