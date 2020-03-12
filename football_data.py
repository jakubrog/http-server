import http.client
import json
from datetime import datetime
import html_generator

connection = http.client.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': 'PASTE_YOUR_API_HERE' }
domain_name = 'http://localhost:8080/'

def set_domain_name(name):
    global domain_name
    domain_name = name

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
    html.add_header("Active competitions")
    get_current_competitions(html)

    return html.get_HTML()

def get_club_list(title='Club List'):
    html = html_generator.Generator(title)
    connection.request('GET', '/v2/teams', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    result = {}
    for i in response['teams']:
        if i['name'] != None:
            result[i['name']] = domain_name + 'teams?id=' + str(i['id'])
    html.add_header('Available clubs')
    html.add_clickable_list(result)
    return html.get_HTML()

def get_club_info(team_id):
    connection.request('GET', '/v2/teams/' + str(team_id), None, headers )
    response = json.loads(connection.getresponse().read().decode())
    html = html_generator.Generator(response['name'])
    get_WLD_stats(team_id, html)
    competitions = {}
    html.add_header("Active competitions:")
    for i in response['activeCompetitions']:
        competitions[i['name']] = domain_name + 'competitions?id=' + str(i['id'])
    html.add_clickable_list(competitions)

    html.add_header("Squad:")
    squad = {}
    for i in response['squad']:
        squad[i['name']] = domain_name + 'players?id=' + str(i['id'])

    html.add_clickable_list(squad)
    
    return html.get_HTML()

def get_current_competitions(html=html_generator.Generator("Active competitions")):
    connection.request('GET', '/v2/competitions', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    result = {}
    for i in response['competitions']:
        if i['currentSeason'] != None and datetime.strptime(i['currentSeason']['endDate'], '%Y-%m-%d') > datetime.today():
            result[i['name']] = domain_name + 'competitions?id=' + str(i['id'])
    html.add_clickable_list(result)
    return html.get_HTML()

# get nb of win, loose and draw matches, home and away
def get_WLD_stats(team_id, html=html_generator.Generator("WLD")):
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
    result = []
    result.append("Home Winner : " + str(home_winner))
    result.append("Home Draw : " + str(home_draw))
    result.append("Home Looser : " + str(home_looser))
    result.append("Away Winner : " + str(away_winner))
    result.append("Away Draw : " + str(away_draw))
    result.append("Away Looser : " + str(away_looser))
    html.add_header("WLD stats")
    html.add_list(result)
    return html.get_HTML()

def get_player_info(player_id):
    connection.request('GET', '/v2/players/' + str(player_id), None, headers)
    player = json.loads(connection.getresponse().read().decode())
    connection.request('GET', '/v2/players/' + str(player_id) + "/matches", None, headers)
    player_matches = json.loads(connection.getresponse().read().decode())
    html = html_generator.Generator(player['name'])
    html.add_header(player['name'])
    html.add_header("Birth: " + player['dateOfBirth'], 4)
    html.add_header("Nationality: " + player['nationality'], 4)
    html.add_header("Position: " + player['position'], 4)
    html.add_header("Played matches: " + str(player_matches['count']), 4)
    return html.get_HTML()

def get_competition_info(competition_id):
    connection.request('GET', '/v2/competitions/' + str(competition_id), None, headers)
    competition = json.loads(connection.getresponse().read().decode())
    html = html_generator.Generator("Not valid API")
    if 'message' in competition.keys():
        html.add_header(competition['message'], 3)
        html.add_header("Error code: " + str(competition['errorCode']), 5)
    else:
        html.add_header(competition['name'], 1)
        html.add_header("Start date: " + competition['currentSeason']['startDate'] , 3)
        html.add_header("End date: " + competition['currentSeason']['endDate'] , 3)
        html.add_header("Area: " + competition['area']['name'], 3)
        html.add_header("Match day: " + str(competition['currentSeason']['currentMatchday']), 3)

    return html.get_HTML()