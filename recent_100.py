"""Recent_100.py

Cache the most recent 100 ranked or normal draft games.

https://developer.riotgames.com/
"""

from riotwatcher import LolWatcher, ApiError


API_KEY = 'RGAPI-bad8c61c-0ee1-473c-8c2b-25d2e52e309a'
# HLGaming
ENCRYPTED_ACCOUNT_ID = '_rOYhaZVY5GLboMPjsiAX1h19weV-ok3IXMZ23VnqESe1J8'
REGION = "NA1"

lol_watcher = LolWatcher(API_KEY)

matchlist = lol_watcher.match.matchlist_by_account(
    REGION,
    ENCRYPTED_ACCOUNT_ID)
'''Queue ids        
{
        "queueId": 420,
        "map": "Summoner's Rift",
        "description": "5v5 Ranked Solo games",
        "notes": null
    },
{
        "queueId": 400,
        "map": "Summoner's Rift",
        "description": "5v5 Draft Pick games",
        "notes": null
    }
'''