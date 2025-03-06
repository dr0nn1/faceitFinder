import requests
import json
from datetime import datetime

# Add your API Key. https://developers.faceit.com/apps
apikey = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX"
baseURL = "https://open.faceit.com/data/v4/"
headers = {'Authorization': f'Bearer {apikey}',
           'accept': 'application/json'}


def app():
    print("All names are case sensitive")
    firstName = input("Enter your name: ")

    try:
        id = findUserId(firstName)
    except:
        print(f'No player with name {firstName} found. Please try again')
        exit()

    secondName = input("Enter the name of the person you are looking for: ")
    try:
        secondId = findUserId(secondName)
    except:
        print(
            f'No player with name {secondName} found. Searching only for name match')
        secondId = None

    totalMatches = int(findTotalGames(id))
    offset = 0
    matches = []
    while len(matches) == 0 and offset < totalMatches+100:
        games = findUserGames(id, offset)
        matches = matchMatches(games, secondName, secondId)
        offset += 100

    if len(matches) == 0:
        print("No matches found")
        exit()

    print(f'You have met in {len(matches)} matches. Here are the links:')
    for match in matches:
        print(f'https://www.faceit.com/en/cs2/room/{match}/scoreboard' + "\n")


def findUserId(name):
    url = f'{baseURL}players?nickname={name}'
    response = requests.get(url=url, headers=headers)
    response_dict = json.loads(response.text)
    return response_dict["player_id"]


def findTotalGames(id):
    url = f'{baseURL}players/{id}/stats/cs2'
    response = requests.get(url=url, headers=headers)
    response_dict = json.loads(response.text)
    return (response_dict['lifetime']['Matches'])


def findUserGames(id, offset):
    print(f'Leter fra match {offset} - {offset+100} ')
    url = f'{baseURL}players/{id}/history?game=cs2&from=0&to={int(datetime.now().timestamp())}]&offset={offset}&limit=100'
    response = requests.get(url=url, headers=headers)
    return json.loads(response.text)


def matchMatches(games, secondName, secondId):
    matches = []
    for game in games['items']:
        for team in game['teams']:
            for player in game['teams'][team]['players']:
                if player['player_id'] == secondId or player['nickname'] == secondName or player['game_player_name'] == secondName:
                    matches.append(game['match_id'])
    return matches


if __name__ == "__main__":
    app()
