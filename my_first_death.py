"""Print the in-game time of my first death for a given account and game."""

from riotwatcher import LolWatcher, ApiError

API_KEY = 'RGAPI-caa0c5c1-4aa8-4270-9462-7e5fc340286f'
HLGAMING_ACCT_ID = '_rOYhaZVY5GLboMPjsiAX1h19weV-ok3IXMZ23VnqESe1J8'
LIGGS_ACCT_ID = 'F8nne3rshXk-_xy5AyAe3jDXm_VwAUSILeTCiWpTvZ9ZOg'
REGION = "NA1"


def last_match_by_acct(acct_id, region=REGION):
    """Get last match info for desired acct."""
    matchlist = lol_watcher.match.matchlist_by_account(
        region, encrypted_account_id=acct_id, begin_index=0
    )
    matches = matchlist['matches']
    last_match_id = matches[0]['gameId']

    return lol_watcher.match.by_id(region, last_match_id)


def my_participant_id(match, acct_id):
    """Get my participant id from match info."""
    participant_ids = match['participantIdentities']
    for user in range(10):
        participant = participant_ids[user]
        participant_id = participant['participantId']
        participant_acct_id = participant['player']['accountId']
        if participant_acct_id == acct_id:
            print("My Participant ID:", participant_id)

            return participant_id



'''# Get `match timeline` from a `match id`
match_timeline = lol_watcher.match.timeline_by_match(REGION, match_id)

"""Returns a list of `frames` and their `duration` from the `match timeline`.

The length of a `match timeline frame` is equal to the 'frameInterval'
(default: 60000 (milliseconds or 60s).

"""
frame_duration = match_timeline['frameInterval']
timeline_frames = match_timeline['frames']
frame_count = len(timeline_frames)


def first_death(f_count=frame_count, frames=timeline_frames):
    """Parse `timeline_frames` for participantFrames, events, and timestamp."""
    for i in range(f_count):
        frame = frames[i]
        participant_frames = frame['participantFrames']
        events = frame['events']
        timestamp = frame['timestamp']
        """Parse events for champion kills and my participant ID."""
        for event in events:
            if event['type'] == 'CHAMPION_KILL' and event['victimId'] == my_participant_id:
                print(event)

                #return event'''


if __name__ == "__main__":

    lol_watcher = LolWatcher(API_KEY)
    last_game = last_match_by_acct(LIGGS_ACCT_ID)
    print(last_game)
    my_participant_id(last_game, LIGGS_ACCT_ID)
    #first_death()
