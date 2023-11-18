import boto3
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def national_team(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'player-stats-l9'

    response = dynamodb.Table(table_name).scan()
    items = response['Items']

    li = get_candidates_for_national_team(items)

    response = {}

    for dict in li:
        for key in dict:
            response[key] = dict[key]

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(response, cls=DecimalEncoder),
    }

def filter_players_by_games_played(data, min_matches=5):
    filtered_players = [player for player in data if player["gamesPlayed"] >= min_matches]
    return filtered_players


def get_sort_key(position, player):
    traditional = player["traditional"]
    advanced = player["advanced"]

    if position == 'pointGuard':
        return advanced["hollingerAssistRatio"], advanced["effectiveFieldGoalPercentage"]
    elif position == 'shootingGuard':
        return (
            advanced["trueShootingPercentage"],
            traditional["threePoints"]["shootingPercentage"]
        )
    elif position in ('smallForward', 'powerForward'):
        return (
            advanced["trueShootingPercentage"],
            traditional["rebounds"]
        )
    elif position == 'center':
        return traditional["rebounds"], traditional["blocks"]
    else:
        return 0, 0

def position_dict(sorted_players):
    result = []
    for key in sorted_players:
        if(key == "PG"):
            iterations = min(len(sorted_players[key]), 3)
            pg = { 'pointGuards': [] }
            for i in range(iterations):
                pg['pointGuards'].append(
                        {
                            "playerName": sorted_players[key][i]["playerName"],
                            "gamesPlayed": sorted_players[key][i]["gamesPlayed"],
                            "hollingerAssistRatio": sorted_players[key][i]["advanced"]["hollingerAssistRatio"],
                            "effectiveFieldGoalPercentage": sorted_players[key][i]["advanced"]["effectiveFieldGoalPercentage"]
                        }
                    )
            result.append(pg)
        elif(key == "SG"):
            iterations = min(len(sorted_players[key]), 3)
            sg = { 'shootingGuards': [] }
            for i in range(iterations):
                sg['shootingGuards'].append(
                        {
                            "playerName": sorted_players[key][i]["playerName"],
                            "gamesPlayed": sorted_players[key][i]["gamesPlayed"],
                            "trueShootingPercentage": sorted_players[key][i]["advanced"]["trueShootingPercentage"],
                            "averageThreePointsPercentage": sorted_players[key][i]["traditional"]["threePoints"]["shootingPercentage"]
                        }
                    )
            result.append(sg)
        elif(key == "SF"):
            iterations = min(len(sorted_players[key]), 3)
            sf = { 'smallForwards': [] }
            for i in range(iterations):
                sf['smallForwards'].append(
                        {
                            "playerName": sorted_players[key][i]["playerName"],
                            "gamesPlayed": sorted_players[key][i]["gamesPlayed"],
                            "trueShootingPercentage": sorted_players[key][i]["advanced"]["trueShootingPercentage"],
                            "rebounds": sorted_players[key][i]["traditional"]["rebounds"]
                        }
                    )
            result.append(sf)
        elif(key == "PF"):
            iterations = min(len(sorted_players[key]), 3)
            pf = { 'powerForwards': [] }
            for i in range(iterations):
                pf['powerForwards'].append(
                        {
                            "playerName": sorted_players[key][i]["playerName"],
                            "gamesPlayed": sorted_players[key][i]["gamesPlayed"],
                            "trueShootingPercentage": sorted_players[key][i]["advanced"]["trueShootingPercentage"],
                            "rebounds": sorted_players[key][i]["traditional"]["rebounds"]
                        }
                    )
            result.append(pf)

        if(key == "C"):
            iterations = min(len(sorted_players[key]), 3)
            c = { 'centers': [] }
            for i in range(iterations):
                c['centers'].append(
                        {
                            "playerName": sorted_players[key][i]["playerName"],
                            "gamesPlayed": sorted_players[key][i]["gamesPlayed"],
                            "rebounds": sorted_players[key][i]["traditional"]["rebounds"],
                            "blocks": sorted_players[key][i]["traditional"]["blocks"]
                        }
                    )
            result.append(c)
    return result

def sort_players_by_position(players_data):
    categorized_players = {}

    for player in players_data:
        position = player["position"]
        if position in categorized_players:
            categorized_players[position].append(player)
        else:
            categorized_players[position] = [player]

    sorted_players = {}

    for position, players in categorized_players.items():
        sorted_players[position] = sorted(players, key=lambda x: get_sort_key(position, x))

        if len(sorted_players[position]) > 3:
            sorted_players[position] = sorted(
                sorted_players[position],
                key=lambda x: (-x["gamesPlayed"], x["playerName"])
            )

    return position_dict(sorted_players)


def get_candidates_for_national_team(data):
    first_filter = filter_players_by_games_played(data)
    sorted_players = sort_players_by_position(first_filter)

    return sorted_players