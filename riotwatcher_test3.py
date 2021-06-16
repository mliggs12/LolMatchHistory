"""RiotWatcher testing.

https://developer.riotgames.com/

Repository: https://github.com/mliggs12/Riot-Watcher
"""

from pprint import pprint as pprint
from riotwatcher import LolWatcher, ApiError


API_KEY = 'RGAPI-45b97163-6390-46a4-a112-3eb49d09dd41'
# Liggs
ACCOUNT_ID = 'F8nne3rshXk-_xy5AyAe3jDXm_VwAUSILeTCiWpTvZ9ZOg'
REGION = "NA1"

lol_watcher = LolWatcher(API_KEY)

me = lol_watcher.summoner.by_account(REGION, ACCOUNT_ID)
my_ranked_stats = lol_watcher.league.by_summoner(REGION, me['id'])

print(my_ranked_stats)

versions = lol_watcher.data_dragon.versions_for_region(REGION)
#champions_version = versions['n']['champion']

print(versions)