"""RiotWatcher testing.

https://developer.riotgames.com/

Repository: https://github.com/mliggs12/Riot-Watcher
"""

from pprint import PrettyPrinter as pp
from riotwatcher import LolWatcher, ApiError


API_KEY = 'RGAPI-bad8c61c-0ee1-473c-8c2b-25d2e52e309a'
# HLGaming
ENCRYPTED_ACCOUNT_ID = '_rOYhaZVY5GLboMPjsiAX1h19weV-ok3IXMZ23VnqESe1J8'
REGION = "NA1"

lol_watcher = LolWatcher(API_KEY)

matchlist = lol_watcher.match.matchlist_by_account(
    region=REGION,
    encrypted_account_id=ENCRYPTED_ACCOUNT_ID,
    begin_index=0)
matches = matchlist['matches']    # 100th match is begin_index: 100 and list index [99]
# Get match id from matchlist index
index = 0
match_id = matches[index]['gameId']

# Get my participant id in the indexed `match`
match = lol_watcher.match.by_id(REGION, match_id)
participant_ids = match['participantIdentities']
for i in range(10):
    participant = participant_ids[i]
    participant_id = participant['participantId']
    participant_acct_id = participant['player']['accountId']
    if participant_acct_id != ENCRYPTED_ACCOUNT_ID:
        pass
    else:
        print("My Participant ID:", participant_id)

# Get `match timeline` from a `match id`
match_timeline = lol_watcher.match.timeline_by_match(REGION, match_id)

"""Returns a list of `frames` and their `duration` from the `match timeline`.

The length of a `match timeline frame` is equal to the 'frameInterval'
(default: 60000 (milliseconds or 60s).

"""
frame_duration = match_timeline['frameInterval']
timeline_frames = match_timeline['frames']
frame_count = len(timeline_frames)

print("""
Frame count: {}
Frame duration: {} ms
""".format(frame_count, frame_duration))
"""Parse `timeline_frames` for participantFrames, events, and timestamp."""
for i in range(frame_count):
    frame = timeline_frames[i]
    participant_frames = frame['participantFrames']
    events = frame['events']
    timestamp = frame['timestamp']
    print("""Frame {}:
    
Participant frames:""".format(i+1))
    for pf in range(10):
        num = str(pf + 1)
        p_frame = participant_frames[num]
        print(num, p_frame)
    print("""
Events: {}
Timestamp: {}
""".format(events, timestamp))

