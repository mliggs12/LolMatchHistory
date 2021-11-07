"""Main interface for the LoLMatchHistory."""
import os
from datetime import datetime
import requests
from tabulate import tabulate
import pandas as pd

# Get your Riot API key from developer.riotgames.com and set in environment variables as 'RIOT_API_KEY'
HEADERS = {'X-Riot-Token': os.environ['RIOT_API_KEY']}  # required headers for API calls
BASE_URL_V4 = "https://na1.api.riotgames.com/lol"  # North America
BASE_URL_V5 = "https://americas.api.riotgames.com/lol"


def get_summoner_puuid_by_name(name="Liggs"):
    """Retrieves your Summoner PUUID using your Summoner Name.
    Your Summoner PUUID is needed to get your matchlist. Defaults to my Summoner Name.

    Endpoint: GET /summoner/v4/summoners/by-name/{summonerName}
    """
    url = f"{BASE_URL_V4}/summoner/v4/summoners/by-name/{name}"
    r = requests.get(url, headers=HEADERS)
    print(f"Requesting PUUID for {name}...")
    if r.status_code != 200:
        print(r.status_code)
    puuid = r.json()['puuid']
    return puuid


def get_match_ids(puuid, count=20):
    """Retrieves a list of match ids using your PUUID. Defaults to 20 match ids.
    Get up to 100 match ids. Match ids are in reverse chronological order.

    Endpoint: GET /match/v5/matches/by-puuid/{puuid}/ids
    """
    url = f"{BASE_URL_V5}/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(r.status_code)
    print(f"Retrieving Player's last {count} Match IDs...")
    return r.json()


def get_matches_by_ids(matches, puuid):
    """Retrieves match information for each match id in list and returns a dataframe.

    Endpoint: GET /match/v5/matches/{matchId}
    """
    print("Retrieving Player's stats for each match...")
    # Empty lists for dataframe creation
    matches_ids = []
    creations = []
    durations = []
    queue_ids = []
    assist_totals = []
    death_totals = []
    kill_totals = []
    kdas = []
    champions = []
    champ_lvls = []
    gold_totals = []
    lanes = []
    champ_dmgs = []
    cs_totals = []
    results = []
    for m_id in matches:
        url = f"{BASE_URL_V5}/match/v5/matches/{m_id}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            status = r.json()
            code = status['status']['status_code']
            msg = status['status']['message']
            print(m_id, code, msg)
        else:
            data = r.json()
            match_id = data['metadata']['matchId']
            matches_ids.append(match_id)

            game_creation = str(data['info']['gameCreation'])[:-3]  # UNIX timestamp
            # Convert unix timestamp to datetime
            ts = int(game_creation)
            game_creation = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            creations.append(game_creation)

            game_duration = data['info']['gameDuration']  # seconds
            # Convert seconds to minutes:seconds, older matches have 7 digits
            if len(str(game_duration)) < 7:
                min, sec = divmod(game_duration, 60)
                game_duration = "%02d:%02d" % (min, sec)
            else:
                sec, ms = divmod(game_duration, 1000)
                min, sec = divmod(sec, 60)
                game_duration = "%02d:%02d" % (min, sec)
            durations.append(game_duration)

            queue_id = data['info']['queueId']  # 420 = ranked, 400 = normal draft
            queue_ids.append(queue_id)

            participants = data['info']['participants']  # detailed info for each player
            # Retrieve your info for the match
            for p in participants:
                if p['puuid'] == puuid:
                    assists = p['assists']
                    assist_totals.append(assists)
                    deaths = p['deaths']
                    death_totals.append(deaths)
                    kills = p['kills']
                    kill_totals.append(kills)
                    champion = p['championName']
                    champions.append(champion)
                    champ_lvl = p['champLevel']
                    champ_lvls.append(champ_lvl)
                    gold_earned = p['goldEarned']
                    gold_totals.append(gold_earned)
                    lane = p['lane']
                    lanes.append(lane)
                    dmg_to_champs = p['totalDamageDealtToChampions']
                    champ_dmgs.append(dmg_to_champs)
                    cs = p['totalMinionsKilled']
                    cs_totals.append(cs)
                    win = p['win']  # bool
                    results.append(win)
                    kda = calc_kda_ratio(kills, assists, deaths)
                    kdas.append(kda)
    matches_info = {
        'match_id': matches_ids,
        'created': creations,
        'duration': durations,
        'queue_id': queue_ids,
        'win': results,
        'champion': champions,
        'lane': lanes,
        'level': champ_lvls,
        'kills': kill_totals,
        'deaths': death_totals,
        'assists': assist_totals,
        'kda': kdas,
        'tot_dmg_to_champs': champ_dmgs,
        'cs': cs_totals,
        'gold_earned': gold_totals,
    }
    df = pd.DataFrame(matches_info)
    return df


def calc_kda_ratio(kills, assists, deaths):
    if deaths != 0:
        return round((kills + assists) / deaths, 2)
    else:
        print(f"Perfect KDA -- K+A: {kills+assists}")
        return None


def main():
    pid = get_summoner_puuid_by_name(name="Bushidobrownn")
    match_ids = get_match_ids(pid, count=5)
    df = get_matches_by_ids(match_ids, pid)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    print(f"Avg. kills: {df['kills'].mean()}")
    print(f"Avg. deaths: {df['deaths'].mean()}")
    print(f"Avg. assists: {df['assists'].mean()}")
    print(f"Avg. KDA: {df['kda'].mean()}")


if __name__ == "__main__":
    main()
