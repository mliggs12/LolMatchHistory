"""Matchhistorycacher.

- Should make this into a class somehow.
"""
import json
from riot_dataclasses import *
import requests


if __name__ == "__main__":
    p.id = p.id
    m_timeline = match_timeline_by_id(match_ids[0])
    timeline_info = m_timeline['info']
    frame_interval = timeline_info['frameInterval']    # 60000 ms or 1 min.
    m_timeline_frames = timeline_info['frames']
    # Parse data for each frame of the match timeline
    frame_count = 0
    for frame in m_timeline_frames:
        frame_count += 1
        # Convert ms to min:sec timestamp
        ms_timestamp = frame['timestamp']
        ts_sec = int((ms_timestamp / 1000) % 60)
        ts_min = int((ms_timestamp / (1000 * 60)) % 60)
        timestamp = f"{ts_min}:{ts_sec}"
        print(f"\nFrame {frame_count} -- End Timestamp: {timestamp}")
        # Parse all of the frame's events
        frame_events = frame['events']
        print(json.dumps(frame_events, indent=4))
        # Parse only event data for the user by participantId
        user_events = []
        for e in frame_events:
            if ("killerId" in e and e['killerId'] == p.id) \
                    or ("victimId" in e and e['victimId'] == p.id) \
                    or ("participantId" in e and e['participantId'] == p.id):
                user_events.append(e)
        # print(f"Events:\n" + json.dumps(user_events, indent=4))
        # State of champion in the current frame
        participant_frames = frame['participantFrames']
        p_info = participant_frames[str(p.id)]
        # print(f"\nFrame {frame_count} -- Participant Info:\n" + json.dumps(p_info, indent=4))
        # Death events for user participant
        for event in user_events:
            if "victimId" in event and event['victimId'] == p.id:
                print(json.dumps(event, indent=4))











