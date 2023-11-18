from flask import abort

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
                players[i]['other']['val'].append(round((int(player_stats[2])+2*int(player_stats[4])+3*int(player_stats[6])+int(player_stats[8])+int(player_stats[9])+int(player_stats[10])+int(player_stats[11]))-(int(player_stats[3])-int(player_stats[2])+int(player_stats[5])-int(player_stats[4])+int(player_stats[7])-int(player_stats[6])+int(player_stats[12])),2))
                players[i]['other']['efg'].append(round((int(player_stats[4])+int(player_stats[6])+0.5*int(player_stats[6]))/(int(player_stats[5])+int(player_stats[7]))*100 if (int(player_stats[5])+int(player_stats[7])) > 0 else 0,2))
                players[i]['other']['shp'].append(round((int(player_stats[2])+2*int(player_stats[4])+3*int(player_stats[6]))/(2*(int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3])))*100 if (2*(int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3]))) > 0 else 0,2))
                players[i]['other']['har'].append(round(int(player_stats[10])/(int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3])+int(player_stats[10])+int(player_stats[12]))*100 if (int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3])+int(player_stats[10])+int(player_stats[12])) > 0 else 0,2))
        
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
                    'valorization' : 0,
                    'effectiveFieldGoalPercentage' : 0,
                    'trueShootingPercentage' : 0,
                    'hollingerAssistRatio' : 0
                },
                'other' : {
                    'val' : [round((int(player_stats[2])+2*int(player_stats[4])+3*int(player_stats[6])+int(player_stats[8])+int(player_stats[9])+int(player_stats[10])+int(player_stats[11]))-(int(player_stats[3])-int(player_stats[2])+int(player_stats[5])-int(player_stats[4])+int(player_stats[7])-int(player_stats[6])+int(player_stats[12])),2)],
                    'efg' : [round((int(player_stats[4])+int(player_stats[6])+0.5*int(player_stats[6]))/(int(player_stats[5])+int(player_stats[7]))*100 if (int(player_stats[5])+int(player_stats[7])) > 0 else 0,2)],
                    'shp' : [round((int(player_stats[2])+2*int(player_stats[4])+3*int(player_stats[6]))/(2*(int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3])))*100 if (2*(int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3]))) > 0 else 0,2)],
                    'har' : [round(int(player_stats[10])/(int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3])+int(player_stats[10])+int(player_stats[12]))*100 if (int(player_stats[5])+int(player_stats[7])+0.475*int(player_stats[3])+int(player_stats[10])+int(player_stats[12])) > 0 else 0,2)]
                },

            }
            players.append(dict)

    #format response
    for i, player in enumerate(players):
        players[i]['traditional']['freeThrows']['made'] = round(players[i]['traditional']['freeThrows']['made']/players[i]['gamesPlayed'], 1)
        players[i]['traditional']['freeThrows']['attempts'] = round(players[i]['traditional']['freeThrows']['attempts']/players[i]['gamesPlayed'], 1)
        players[i]['traditional']['freeThrows']['shootingPercentage'] = round(players[i]['traditional']['freeThrows']['made']/players[i]['traditional']['freeThrows']['attempts']*100 if (players[i]['traditional']['freeThrows']['attempts']) > 0 else 0, 1)

        players[i]['traditional']['twoPoints']['made'] = round(players[i]['traditional']['twoPoints']['made']/players[i]['gamesPlayed'], 1)
        players[i]['traditional']['twoPoints']['attempts'] = round(players[i]['traditional']['twoPoints']['attempts']/players[i]['gamesPlayed'], 1)
        players[i]['traditional']['twoPoints']['shootingPercentage'] = round(players[i]['traditional']['twoPoints']['made']/players[i]['traditional']['twoPoints']['attempts']*100 if (players[i]['traditional']['twoPoints']['attempts']) > 0 else 0, 1)

        players[i]['traditional']['threePoints']['made'] = round(players[i]['traditional']['threePoints']['made']/players[i]['gamesPlayed'], 1)
        players[i]['traditional']['threePoints']['attempts'] = round(players[i]['traditional']['threePoints']['attempts']/players[i]['gamesPlayed'], 1)
        players[i]['traditional']['threePoints']['shootingPercentage'] = round(players[i]['traditional']['threePoints']['made']/players[i]['traditional']['threePoints']['attempts']*100 if (players[i]['traditional']['threePoints']['attempts']) > 0 else 0, 1)

        players[i]['traditional']['points'] = round((players[i]['traditional']['freeThrows']['made']+2*players[i]['traditional']['twoPoints']['made']+3*players[i]['traditional']['threePoints']['made'])/players[i]['gamesPlayed'] if (players[i]['gamesPlayed']) > 0 else 0, 1)
        players[i]['traditional']['rebounds'] = round(players[i]['traditional']['rebounds']/players[i]['gamesPlayed'] if (players[i]['gamesPlayed']) > 0 else 0,1)
        players[i]['traditional']['blocks'] = round(players[i]['traditional']['blocks']/players[i]['gamesPlayed'] if (players[i]['gamesPlayed']) > 0 else 0,1)
        players[i]['traditional']['assists'] = round(players[i]['traditional']['assists']/players[i]['gamesPlayed'] if (players[i]['gamesPlayed']) > 0 else 0,1)
        players[i]['traditional']['steals'] = round(players[i]['traditional']['steals']/players[i]['gamesPlayed'] if (players[i]['gamesPlayed']) > 0 else 0,1)
        players[i]['traditional']['turnovers'] = round(players[i]['traditional']['turnovers']/players[i]['gamesPlayed'] if (players[i]['gamesPlayed']) > 0 else 0,1)
        
        players[i]['advanced']['valorization'] = round(sum(players[i]['other']['val'])/players[i]['gamesPlayed'] if (players[i]['gamesPlayed']) > 0 else 0,1)
        players[i]['advanced']['effectiveFieldGoalPercentage'] = round(sum(players[i]['other']['efg'])/players[i]['gamesPlayed'] if (players[i]['gamesPlayed']) > 0 else 0,1)
        players[i]['advanced']['trueShootingPercentage'] = round(sum(players[i]['other']['shp'])/players[i]['gamesPlayed'] if (players[i]['gamesPlayed']) > 0 else 0,1)
        players[i]['advanced']['hollingerAssistRatio'] = round(sum(players[i]['other']['har'])/players[i]['gamesPlayed'] if (players[i]['gamesPlayed']) > 0 else 0,1)
    
        players[i].pop('other')
    return players