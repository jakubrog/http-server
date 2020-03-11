import http.client
import json
from datetime import datetime
import html_generator

connection = http.client.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': '531e6778b6594ef4bbe09a753d6c2b52' }

def get_club_selection(query_name, action, title="Club selection"):
    html = html_generator.Generator(title)
    html.add_header('Select one team')
    connection.request('GET', '/v2/teams', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    result = {}
    for i in response['teams']:
        if i['name']:
            result[i['name']] = str(i['id'])
    html.add_select_from_list(query_name, action, result)
    return html.get_HTML()

def get_club_list(title='Club List'):
    html = html_generator.Generator(title)
    connection.request('GET', '/v2/teams', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    result = []
    for i in response['teams']:
        print('')
        if i['name'] != None:
            result.append(i['name'] + ' : ' + str(i['id']))
    html.add_header('Avaiavble clubs')
    html.add_list(result)
    return html.get_HTML()

def get_club_info(team_id):
    connection.request('GET', '/v2/teams/' + str(team_id), None, headers )
    response = json.loads(connection.getresponse().read().decode())
    html = html_generator.Generator(response['name'])
    # TODO: CONTINUE TO CREATING HTMLs
    for i in response['activeCompetitions']:
        print(i['name'])

    print("\nSQUAD:")
    for i in response['squad']:
        print(i['name'])

    
def get_current_competitions():
    connection.request('GET', '/v2/competitions', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    result = ""
    for i in response['competitions']:
        if i['currentSeason'] != None and datetime.strptime(i['currentSeason']['endDate'], '%Y-%m-%d') > datetime.today():
            result += str(i['id']) + " " +i['name'] + " : " +  i['currentSeason']['endDate'] + ' - ' + i['currentSeason']['endDate'] + "\n"
    return result

# get nb of win, loose and draw matches, homa and away
def get_WLD_stats(team_id):
    connection.request('GET', '/v2/teams/' + str(team_id) + "/matches", None, headers)
    response = json.loads(connection.getresponse().read().decode())
    home_winner, home_looser, home_draw = 0, 0, 0
    away_winner, away_looser, away_draw = 0, 0, 0
    for i in response['matches']:
        if  i['homeTeam']['id'] == team_id:
            if i['score']['winner'] == 'HOME_TEAM':
                home_winner += 1
            elif i['score']['winner'] == 'AWAY_TEAM':
                home_looser += 1
            elif i['score']['winner'] == 'DRAW':
                home_draw += 1
        else:
            if i['score']['winner'] == 'AWAY_TEAM':
                away_winner += 1
            elif i['score']['winner'] == 'HOME_TEAM':
                away_looser += 1
            elif i['score']['winner'] == 'DRAW':
                away_draw += 1

    return home_winner, away_winner, home_looser, away_looser, home_draw, away_draw

# get player name, birthday, country and nb of matches
def get_player_info(player_id):
    connection.request('GET', '/v2/players/' + str(player_id), None, headers)
    player = json.loads(connection.getresponse().read().decode())

    connection.request('GET', '/v2/players/' + str(player_id) + "/matches", None, headers)
    player_matches = json.loads(connection.getresponse().read().decode())
    print(player_matches['count'])
    