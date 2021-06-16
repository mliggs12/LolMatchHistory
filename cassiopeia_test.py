"""Cassiopeia_Test.py"""

import cassiopeia as cass

cass.set_riot_api_key("RGAPI-4229d7f6-972e-44d1-831b-eefa233bc31b")

bushido = cass.get_summoner(name="Bushidobrownn", region="NA")

match = cass.Match(platform="NA1", id=3714620977)


stats = cass.core.staticdata.champion.Stats()

print(bushido.match_history[0])
print(stats.armor)