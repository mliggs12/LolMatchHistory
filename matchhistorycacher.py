"""Matchhistorycacher"""

import requests
import json


API_KEY = 'RGAPI-82a89de9-c58a-4e1a-8c74-49a9a18aa755'
ACCT_ID = 'F8nne3rshXk-_xy5AyAe3jDXm_VwAUSILeTCiWpTvZ9ZOg'

API_URL_BASE = 'https://na1.api.riotgames.com/lol/'
MATCHLIST_URL_END = 'match/v4/matchlists/by-account/'
FILE_PATH = 'C:/Files/Code/Projects/matchhistorycacher/test3.txt'


def GET_matchlist(begin_index):
    '''GET request to Match-V4 API, returns MatchlistDto as JSON stream.
    
    Paginates using beginIndex until the end of a liggs' matchlist.
    '''
    matchlist_url = API_URL_BASE + MATCHLIST_URL_END + ACCT_ID + '?queue=420' + '&beginIndex=' + str(begin_index) + '&api_key=' + API_KEY

    matchlist = requests.get(matchlist_url).json()
    return matchlist

def JSON_to_file(file_path, json_stream):
    '''Writes a JSON stream to a file.'''
    with open(file_path, 'a') as fp:
        json.dump(json_stream, fp, indent = 4)

def read_JSON_file(file_path):
    '''Reads complete file containing JSON.'''
    with open(file_path, 'r') as fp:
        return json.load(fp)


def main():
    '''Main entry point for script.
    
    Currently will overwrite the file.
    '''
    begin_index = 0
    the_matchlist = []
           
    matchlist = GET_matchlist(begin_index)
    if matchlist["matches"] != []:
        the_matchlist.append(matchlist)
        begin_index += 100
    else:
        JSON_to_file(FILE_PATH, the_matchlist)
        print("Complete.")

    

    matchlist = read_JSON_file(FILE_PATH)
    print(matchlist[10])


if __name__ == "__main__":
    main()