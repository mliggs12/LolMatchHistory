"""Summoner.py

    Get a `Summoner` by a summoner name.
"""
from datetime import datetime
import requests

API_KEY = 'RGAPI-1168cf0f-c2ae-4bb5-a8ea-5d8fb5f678bb'
HEADERS = {'X-Riot-Token': API_KEY}
NAME = 'Liggs'


def summoner_by_name(summoner_name=NAME):
    """Takes a valid summoner name and makes request to Summoner-V4 API."""
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"

    return requests.get(url, headers=HEADERS).json()


class Summoner:

    def __init__(self):
        """Save `Summoner` data to object."""
        summoner = summoner_by_name()

        self.name = summoner['name']
        self.profile_icon = summoner['profileIconId']
        self.revision_date = summoner['revisionDate']
        self.summoner_level = summoner['summonerLevel']
        self.summoner_id = summoner['id']
        self.puuid = summoner['puuid']

    def epoch_to_datetime(self):
        epoch_time = self.revision_date / 1000

        return datetime.fromtimestamp(epoch_time)


if __name__ == "__main__":

    liggs = Summoner()
    print(f"Name: {liggs.name}\nProfile icon: {liggs.profile_icon}\n"
          f"Summoner level: {liggs.summoner_level}\nLast updated: {liggs.epoch_to_datetime()}\n"
          f"Summoner ID: {liggs.summoner_id}\nPUUID: {liggs.puuid}")
