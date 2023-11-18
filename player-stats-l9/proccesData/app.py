import json
import boto3
import csv
from io import StringIO
from decimal import Decimal
import math

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('player-stats-l9')

data =[]


def procces_data(event, context):
    global data
    file = s3.get_object(Bucket='player-files-l9', Key='L9HackathonPlayersInput.csv')

    load_data(file)
    players = load_all_data(data)
    for player in players:
        player = json.loads(json.dumps(player), parse_float=Decimal)
        table.put_item(Item=player)

    # print(load_all_data(data))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": players,
        }),
    }


def load_data(file):
    global data
    file_content = file['Body'].read().decode('utf-8')
    
    # Assuming it's a CSV file, parse the CSV content
    csv_reader = csv.reader(StringIO(file_content))
    i=0
    # Process the CSV data (example: printing rows)
    for row in csv_reader:
        if i == 0:
            i+=1
            continue
        
        data.append(row)

def round_half_up(n, decimals=0):
    multiplier = 10**decimals
    return math.floor(n * multiplier + 0.5) / multiplier
# calculating statistics for API endpoint
def loadAllData(data):
    players = []
    #going through csv data, calcuating simple stats
    for player_stats in data:
        playerExist = False
        for i, player in enumerate(players):
            if players[i]['playerName'] == player_stats[0]:
                playerExist = True
                players[i]['gamesPlayed'] += 1
                #sum simple stats
                players[i]['traditional']['freeThrows']['made'] += int(player_stats[2])
                players[i]['traditional']['freeThrows']['attempts'] += int(player_stats[3])
                players[i]['traditional']['twoPoints']['made'] += int(player_stats[4])
                players[i]['traditional']['twoPoints']['attempts'] += int(player_stats[5])
                players[i]['traditional']['threePoints']['made'] += int(player_stats[6])
                players[i]['traditional']['threePoints']['attempts'] += int(player_stats[7])
                players[i]['traditional']['rebounds'] += int(player_stats[8])
                players[i]['traditional']['blocks'] += int(player_stats[9])
                players[i]['traditional']['assists'] += int(player_stats[10])
                players[i]['traditional']['steals'] += int(player_stats[11])
                players[i]['traditional']['turnovers'] += int(player_stats[12])
                #calculating advanced stats
                players[i]['other']['val'].append((int(player_stats[2])+2*int(player_stats[4])+3*int(player_stats[6])+int(player_stats[8])+int(player_stats[9])+int(player_stats[10])+int(player_stats[11]))-(int(player_stats[3])-int(player_stats[2])+int(player_stats[5])-int(player_stats[4])+int(player_stats[7])-int(player_stats[6])+int(player_stats[12])))
                players[i]['other']['efg'].append((int(player_stats[4])+int(player_stats[6])+0.5*int(player_stats[6]))/(int(player_stats[5])+int(player_stats[7]))*100 if (int(player_stats[5])+int(player_stats[7])) > 0 else 0)
                players[i]['other']['shp'].append((int(player_stats[2])+2*int(player_stats[4])+3*int(player_stats[6]))/(2*(int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3])))*100 if (2*(int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3]))) > 0 else 0)
                players[i]['other']['har'].append(int(player_stats[10])/(int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3])+int(player_stats[10])+int(player_stats[12]))*100 if (int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3])+int(player_stats[10])+int(player_stats[12])) > 0 else 0)
        
        if(playerExist == False):
            dict = {
                'playerName' : player_stats[0],     
                'position' : player_stats[1],
                'gamesPlayed': 1,
                'traditional': {
                    'freeThrows': {
                    'attempts' : int(player_stats[3]),
                    'made' : int(player_stats[2]),
                    'shootingPercentage' : 0,
                },
                'twoPoints' : {
                    'attempts' : int(player_stats[5]),
                    'made' : int(player_stats[4]),
                    'shootingPercentage' : 0,
                },
                'threePoints' : {
                    'attempts' : int(player_stats[7]),
                    'made' : int(player_stats[6]),
                    'shootingPercentage' : 0,
                },
                'points' : 0,
                'rebounds' : int(player_stats[8]),
                'blocks' : int(player_stats[9]),
                'assists' : int(player_stats[10]),
                'steals' : int(player_stats[11]),
                'turnovers' : int(player_stats[12]),
                },
                'advanced' : {
                    'valorization' : None,
                    'effectiveFieldGoalPercentage' : None,
                    'trueShootingPercentage' : None,
                    'hollingerAssistRatio' : None
                },
                'other' : {
                    'val' : [((int(player_stats[2])+2*int(player_stats[4])+3*int(player_stats[6])+int(player_stats[8])+int(player_stats[9])+int(player_stats[10])+int(player_stats[11]))-(int(player_stats[3])-int(player_stats[2])+int(player_stats[5])-int(player_stats[4])+int(player_stats[7])-int(player_stats[6])+int(player_stats[12])))],
                    'efg' : [(int(player_stats[4])+int(player_stats[6])+0.5*int(player_stats[6]))/(int(player_stats[5])+int(player_stats[7]))*100 if (int(player_stats[5])+int(player_stats[7])) > 0 else 0],
                    'shp' : [(int(player_stats[2])+2*int(player_stats[4])+3*int(player_stats[6]))/(2*(int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3])))*100 if (2*(int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3]))) > 0 else 0],
                    'har' : [int(player_stats[10])/(int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3])+int(player_stats[10])+int(player_stats[12]))*100 if (int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3])+int(player_stats[10])+int(player_stats[12])) > 0 else 0]
                },

            }
            players.append(dict)

    #format response
    for i, player in enumerate(players):
        playedGames = players[i]['gamesPlayed']

        ftm = players[i]['traditional']['freeThrows']['made']
        fta = players[i]['traditional']['freeThrows']['attempts']
        players[i]['traditional']['freeThrows']['made'] = round_half_up(ftm/playedGames, 1)
        players[i]['traditional']['freeThrows']['attempts'] = round_half_up(fta/playedGames, 1)
        players[i]['traditional']['freeThrows']['shootingPercentage'] = round_half_up(ftm/fta*100 if fta > 0 else 0, 1)
        
        pm2 = players[i]['traditional']['twoPoints']['made']
        pa2 = players[i]['traditional']['twoPoints']['attempts']
        players[i]['traditional']['twoPoints']['made'] = round_half_up(pm2/playedGames, 1)
        players[i]['traditional']['twoPoints']['attempts'] = round_half_up(pa2/playedGames, 1)
        players[i]['traditional']['twoPoints']['shootingPercentage'] = round_half_up(pm2/pa2*100 if pa2 > 0 else 0, 1)

        pm3 = players[i]['traditional']['threePoints']['made']
        pa3 = players[i]['traditional']['threePoints']['attempts']
        players[i]['traditional']['threePoints']['made'] = round_half_up(pm3/playedGames, 1)
        players[i]['traditional']['threePoints']['attempts'] = round_half_up(pa3/playedGames, 1)
        players[i]['traditional']['threePoints']['shootingPercentage'] = round_half_up(pm3/pa3*100 if pa3 > 0 else 0, 1)

        points = (ftm/playedGames+2*pm2/playedGames+3*pm3/playedGames)
        players[i]['traditional']['points'] = round_half_up(points, 1)
        reb = players[i]['traditional']['rebounds']
        blk = players[i]['traditional']['blocks']
        ass = players[i]['traditional']['assists']
        stl = players[i]['traditional']['steals']
        trn = players[i]['traditional']['turnovers']
        players[i]['traditional']['rebounds'] = round_half_up(reb/playedGames if (playedGames) > 0 else 0,1)
        players[i]['traditional']['blocks'] = round_half_up(blk/playedGames if (playedGames) > 0 else 0,1)
        players[i]['traditional']['assists'] = round_half_up(ass/playedGames if (playedGames) > 0 else 0,1)
        players[i]['traditional']['steals'] = round_half_up(stl/playedGames if (playedGames) > 0 else 0,1)
        players[i]['traditional']['turnovers'] = round_half_up(trn/playedGames if (playedGames) > 0 else 0,1)
        
        players[i]['advanced']['valorization'] = round_half_up((points + reb/playedGames + blk/playedGames + ass/playedGames + stl/playedGames) - (fta/playedGames - ftm/playedGames + pa2/playedGames - pm2/playedGames + pa3/playedGames - pm3/playedGames + trn/playedGames),1)
        players[i]['advanced']['effectiveFieldGoalPercentage'] = round_half_up((pm2/playedGames + 1.5 * pm3/playedGames) / (pa2/playedGames + pa3/playedGames) * 100 if (pa2/playedGames + pa3/playedGames) > 0 else 0, 1)
        attempts_ratio = pa2/playedGames + pa3/playedGames + 0.475 * fta/playedGames
        players[i]['advanced']['trueShootingPercentage'] = round_half_up(points / (2 * attempts_ratio) * 100 if (2 * attempts_ratio) > 0 else 0,1)

        har = ((ass/playedGames)/(pa2/playedGames+pa3/playedGames + 0.475*(fta/playedGames)+ass/playedGames+trn/playedGames)*100 if (pa2/playedGames+pa3/playedGames + 0.475*(fta/playedGames)+ass/playedGames+trn/playedGames) > 0 else 0)
        players[i]['advanced']['hollingerAssistRatio'] = round_half_up(har,1)
    

        players[i].pop('other')

    return players