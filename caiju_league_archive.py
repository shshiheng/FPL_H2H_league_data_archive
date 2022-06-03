
import urllib, json, ssl
import urllib.request
import pandas as pd
ssl._create_default_https_context = ssl._create_unverified_context

league_code = 333474
gw_current = 1
gw_start = 1

gw_start=gw_start-1
currpage=1
players = {}
teams = {}
df = []

base = "https://fantasy.premierleague.com/api/bootstrap-static/"
page = urllib.request.urlopen(base)
dataGeneral = json.load(page)
events = dataGeneral["events"]
elements = dataGeneral["elements"]

for j in range(0, 38):
    if dataGeneral['events'][j].get('is_current') == True:
        gw_current = j+1
        break

def getPlayerName(playerID):
    i = 0
    while i < len(elements):
        if (elements[i]["id"] == playerID):
            if(elements[i]["second_name"]=="dos Santos Aveiro"):
                return "Ronaldo"
            if (elements[i]["second_name"] == "Borges Fernandes"):
                return "Fernandes"
            if (elements[i]["second_name"] == "Veiga de Carvalho e Silva"):
                return "Bernardo"
            if elements[i]["second_name"] == "Gato Alves Dias":
                return "Dias"
            if elements[i]["second_name"] == "Rodrigues Moura da Silva":
                return "Lucas Moura"
            if elements[i]["second_name"] == "de Andrade":
                return "Richarlison"
            return (elements[i]["second_name"])
            #return (elements[i]["first_name"] + " " + elements[i]["second_name"])
        i += 1
    return "ID not found"

def getPlayerSelected(playerID):
    i = 0
    while i < len(elements):
        if (elements[i]["id"] == playerID):
            return (elements[i]["selected_by_percent"])
        i += 1
    return "ID not found"


while True:
    league_url = "https://fantasy.premierleague.com/api/leagues-classic/%d/standings/?page_new_entries=1&page_standings=%d&phase=1" % (league_code,currpage)
    response = urllib.request.urlopen(league_url)
    data = json.loads(response.read())
    for i in range(len(data.get('standings').get('results'))):
        team_id = data.get('standings').get('results')[i].get('entry')
        player_name = data.get('standings').get('results')[i].get('player_name')
        team_name = data.get('standings').get('results')[i].get('entry_name')
        players[team_id] = player_name
        teams[team_id] = team_name
    currpage+=1
    if(data.get('standings').get('has_next'))==False:
        break

rank=0
prev=-1
buffer=0
df = pd.DataFrame(columns=['ID', 'Team Name', 'Player Name', 'Bank','Chip', 'Captain', 'Diff Players', 'GW points', 'Total'])
for team_id in players.keys():
    team_url = "https://fantasy.premierleague.com/api/entry/" + str(team_id) + "/event/" + str(gw_current) + "/picks/"
    team_page = urllib.request.urlopen(team_url)
    team_gw_data = json.load(team_page)
    team_inbank = team_gw_data.get('entry_history').get('bank') /10
    team_chip = team_gw_data.get('active_chip')
    team_transfers = team_gw_data.get('entry_history').get('event_transfers')
    team_transfers_cost = -team_gw_data.get('entry_history').get('event_transfers_cost')
    team_gw_points = team_gw_data.get('entry_history').get('points') + team_transfers_cost
    team_total_points = team_gw_data.get('entry_history').get('total_points')
    diff_players = 0
    for j in range(0, 15):
        if team_gw_data["picks"][j]["is_captain"] == True:
            team_captain = getPlayerName(team_gw_data['picks'][j].get('element'))
        if team_gw_data["picks"][j]["multiplier"] > 0:
            selected_by_percent = getPlayerSelected(team_gw_data['picks'][j].get('element'))
            if float(selected_by_percent) <= 5.0:
                diff_players += 1

    total = team_total_points
    if(total!=prev):
        prev=total
        rank+=buffer+1
        buffer=0
    else:
        buffer+=1

    d = pd.DataFrame({'ID': team_id, 'Team Name':teams[team_id], 'Player Name':players[team_id], 'Bank':team_inbank, 'Chip':team_chip, 'Captain': team_captain, 'Diff Players': diff_players, 'GW points':team_gw_points, 'Total':team_total_points}, index=[rank])
    df = df.append(d)
df = df.sort_values(['Total'], ascending=False)

#print(df)

outputpath='caiju_standing.xlsx'
df.to_excel(outputpath,index=True,header=True)