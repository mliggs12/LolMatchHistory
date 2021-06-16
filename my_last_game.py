"""Print the in-game time of my first death for a given account and game."""

import requests

API_KEY = 'RGAPI-caa0c5c1-4aa8-4270-9462-7e5fc340286f'
HLGAMING_ACCT_ID = '_rOYhaZVY5GLboMPjsiAX1h19weV-ok3IXMZ23VnqESe1J8'
LIGGS_ACCT_ID = 'F8nne3rshXk-_xy5AyAe3jDXm_VwAUSILeTCiWpTvZ9ZOg'
LIGGS_PUUID = 'KcjCE8Bq5WQvq988sErZaNMKJNEIqYOvPLMG_WOc-A4Jb0xcrRLCGvEsbfNkjNADjohYl1PO9f-trg'
BASE_URL = 'https://americas.api.riotgames.com/lol/'


def match_ids_by_puuid(puuid, start=0, count=20, api_key=API_KEY):
    """Get list of `match ids` using new v5.

    Start and count are default; count valid values: 0 to 100.
    """
    url = BASE_URL + f'match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}&api_key={api_key}'

    return requests.get(url).json()


def match_by_match_id(match_id, api_key=API_KEY):
    """Get game and participant info using a `match id`.

    returns: `match` obj. (dict., JSON)
    """
    url = BASE_URL + f'match/v5/matches/{match_id}?api_key={api_key}'

    return requests.get(url).json()


def user_match_info(match, puuid):
    """Parse user info from a `match` obj. using global PUUID.

    returns: `Player` obj.
    """
    participants = match['info']['participants']
    for user in participants:
        if user['puuid'] == puuid:
            summoner_name = user['summonerName']
            participant_id = user['participantId']
            champion = user['championName']
            win = user['win']
            time_played = user['timePlayed']
            level = int(user['champLevel'])
            gold = int(user['goldEarned'])
            cs = int(user['totalMinionsKilled'])
            kills = int(user['kills'])
            deaths = int(user['deaths'])
            assists = int(user['assists'])
            dmg_to_champs = int(user['totalDamageDealtToChampions'])

            return Participant(summoner_name, participant_id, champion, win,
                               time_played, level, gold, cs, kills, deaths, assists, dmg_to_champs)


class Participant(object):
    """Holds useful user info from a `match` obj."""
    def __init__(self, summoner_name, participant_id, champion, win, time_played,
                 level, gold, cs, kills, deaths, assists, dmg_to_champs):
        self.summoner_name = summoner_name
        self.participant_id = participant_id
        self.champion = champion
        self.win = win
        self.time_played = time_played
        self.level = level
        self.gold = gold
        self.cs = cs
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.dmg_to_champs = dmg_to_champs

    def kda(self):
        """Calculates the participants K/D/A ratio for the `match`.

        returns: float
        """
        kda = round((self.kills + self.assists) / self.deaths, 2)

        print(f"{self.summoner_name}\n{self.champion}\nK/D/A: {self.kills}/{self.deaths}/{self.assists} ({kda})")


if __name__ == "__main__":

    puuid = LIGGS_PUUID

    match_ids = match_ids_by_puuid(puuid)
    match = match_by_match_id(match_ids[0])
    liggs = user_match_info(match, puuid)

    liggs.kda()