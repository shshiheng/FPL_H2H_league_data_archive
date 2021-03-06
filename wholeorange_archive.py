import urllib, json
import ssl
import urllib.request
import pandas as pd
ssl._create_default_https_context = ssl._create_unverified_context

#247148 3988  249673
league_code = 2241694
gw_current = 14
gw_start = 1

gw_start = gw_start - 1
currpage = 1
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

# class Orange_players():
    

def getPlayerName(playerID):
    i = 0
    while i < len(elements):
        if elements[i]["id"] == playerID:
            if elements[i]["second_name"] == "dos Santos Aveiro":
                return "Ronaldo"
            if elements[i]["second_name"] == "Borges Fernandes":
                return "Fernandes"
            if elements[i]["second_name"] == "Veiga de Carvalho e Silva":
                return "Bernardo"
            if elements[i]["second_name"] == "Gato Alves Dias":
                return "Dias"
            if elements[i]["second_name"] == "Rodrigues Moura da Silva":
                return "Lucas Moura"
            if elements[i]["second_name"] == "de Andrade":
                return "Richarlison"
            return elements[i]["second_name"]
            # return (elements[i]["first_name"] + " " + elements[i]["second_name"])
        i += 1
    return "ID not found"

df = pd.DataFrame(
    columns=['rank', 'ID', 'Team Name', 'Player Name', 'Win', 'Draw', 'Lose', 'GW points',
             'League Points','FPL Points since h2h starts', 'Total FPL Points','Last rank',
             'Rank improve', 'Captain', 'Chip', 'Bank',
             'Total Team Value', 'Transfers', 'Transfer cost', 'Points on Bench', 'Overall rank'])

while True:
    league_url = "https://fantasy.premierleague.com/api/leagues-h2h/%d/standings/?page_new_entries=1&page_standings=%d&phase=1" % (
    league_code, currpage)
    response = urllib.request.urlopen(league_url)
    data = json.loads(response.read())
    for i in range(len(data.get('standings').get('results'))):
        player_team_id = data.get('standings').get('results')[i].get('entry')

        team_url = "https://fantasy.premierleague.com/api/entry/" + str(player_team_id) + "/event/" + str(
            gw_current) + "/picks/"
        team_page = urllib.request.urlopen(team_url)
        team_gw_data = json.load(team_page)
        team_inbank = team_gw_data.get('entry_history').get('bank') / 10
        team_value = team_gw_data.get('entry_history').get('value') / 10
        team_chip = team_gw_data.get('active_chip')
        team_benchpoints = team_gw_data.get('entry_history').get('points_on_bench')
        team_transfers = team_gw_data.get('entry_history').get('event_transfers')
        team_transfers_cost = -team_gw_data.get('entry_history').get('event_transfers_cost')
        team_gw_points = team_gw_data.get('entry_history').get('points') + team_transfers_cost
        team_total_points = team_gw_data.get('entry_history').get('total_points')
        team_overall_rank = team_gw_data.get('entry_history').get('overall_rank')
        for j in range(0, 15):
            if team_gw_data["picks"][j]["is_captain"] == True:
                team_captain = getPlayerName(team_gw_data['picks'][j].get('element'))
                break

        player_name = data.get('standings').get('results')[i].get('player_name')
        team_name = data.get('standings').get('results')[i].get('entry_name')
        rank = data.get('standings').get('results')[i].get('rank')
        last_rank = data.get('standings').get('results')[i].get('last_rank')
        rank_improve = last_rank - rank
        standing_points= data.get('standings').get('results')[i].get('total')
        matches = data.get('standings').get('results')[i].get('matches_played')
        won = data.get('standings').get('results')[i].get('matches_won')
        drawn = data.get('standings').get('results')[i].get('matches_drawn')
        lost = data.get('standings').get('results')[i].get('matches_lost')
        total_league_points = data.get('standings').get('results')[i].get('points_for')

        d = pd.DataFrame({ 'rank': rank, 'ID': player_team_id, 'Team Name': team_name, 'Player Name': player_name,
                           'Win': won, 'Draw': drawn, 'Lose': lost, 'GW points': team_gw_points,
                           'League Points': standing_points, 'FPL Points since h2h starts': total_league_points,
                           'Total FPL Points': team_total_points, 'Last rank': last_rank, 'Rank improve': rank_improve,
                           'Captain': team_captain,  'Chip': team_chip, 'Bank': team_inbank,
                           'Total Team Value': team_value, 'Transfers': team_transfers, 'Transfer cost':team_transfers_cost,
                           'Points on Bench': team_benchpoints,
                            'Overall rank':team_overall_rank}, index=[rank])
        df = df.append(d)
    currpage += 1
    if (data.get('standings').get('has_next')) == False:
        break


# for team_id in players.keys():
#     team_url = "https://fantasy.premierleague.com/api/entry/" + str(team_id) + "/event/" + str(gw_current) + "/picks/"
#     team_page = urllib.request.urlopen(team_url)
#     team_gw_data = json.load(team_page)
#     team_inbank = team_gw_data.get('entry_history').get('bank') /10
#     team_value = team_gw_data.get('entry_history').get('value') /10
#     team_chip = team_gw_data.get('active_chip')
#     team_benchpoints = team_gw_data.get('entry_history').get('points_on_bench')
#     team_transfers = team_gw_data.get('entry_history').get('event_transfers')
#     team_transfers_cost = -team_gw_data.get('entry_history').get('event_transfers_cost')
#     team_gw_points = team_gw_data.get('entry_history').get('points') + team_transfers_cost
#     team_total_points = team_gw_data.get('entry_history').get('total_points')
#     team_overall_rank = team_gw_data.get('entry_history').get('overall_rank')
#     for j in range(0, 15):
#         if team_gw_data["picks"][j]["is_captain"] == True:
#             team_captain = getPlayerName(team_gw_data['picks'][j].get('element'))
#             break
#
#     team_lastweektotal = team_total_points - team_gw_points
#
#     total = team_total_points
#     if (total != prev):
#         prev = total
#         rank += buffer + 1
#         buffer = 0
#     else:
#         buffer += 1
#
#     d = pd.DataFrame({'Team Name': teams[team_id], 'Player Name': players[team_id], 'GW points': team_gw_points,
#                       'Total': team_total_points, 'Captain': team_captain, 'Chip': team_chip, 'Bank': team_inbank,
#                       'Total Team Value': team_value, 'Transfers': team_transfers, 'Transfer cost': team_transfers_cost,
#                       'Points on Bench': team_benchpoints, 'Overall rank': team_overall_rank,
#                       'Lastweekpts': team_lastweektotal}, index=[rank])
#     df = df.append(d)
#
# data_lastweek_league_rank = df.Lastweekpts.rank(method='min', ascending=0).astype(int)
# df = df.assign(lastweek_rank=lambda x: data_lastweek_league_rank)
# data_current_league_rank = df.Total.rank(method='min', ascending=0).astype(int)
# df = df.assign(rank_improve=lambda x: data_lastweek_league_rank - data_current_league_rank)
#
#
#
#
#
# df = df.sort_values(['rank'], ascending=True)

print(df)

outputpath='h2h_standing.xlsx'
df.to_excel(outputpath,index=True,header=True)