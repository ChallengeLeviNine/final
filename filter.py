def filter_players_by_games_played(data, min_matches=5):
    filtered_players = [player for player in data if player["gamesPlayed"] >= min_matches]
    return filtered_players


def get_sort_key(position, player):
    traditional = player["traditional"]
    advanced = player["advanced"]

    if position == 'pointGuard':
        return traditional["assists"], advanced["hollingerAssistRatio"]
    elif position == 'shootingGuard':
        return (
            traditional["twoPoints"]["shootingPercentage"],
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


def extract_position_data(players, position):
    return [
        {
            "playerName": player["playerName"],
            "gamesPlayed": player["gamesPlayed"],
            **player["traditional"],
            **player["advanced"]
        }
        for player in players[position]
    ]


def sort_players_by_position(players_data):
    categorized_players = {}

    for player in players_data:
        position = player["position"]
        categorized_players.setdefault(position, []).append(player)

    sorted_players = {}

    for position, players in categorized_players.items():
        sorted_players[position] = sorted(players, key=lambda x: get_sort_key(position, x))

        if len(sorted_players[position]) > 3:
            sorted_players[position] = sorted(
                sorted_players[position],
                key=lambda x: (x["gamesPlayed"], x["playerName"])
            )

    return sorted_players


def get_candidates_for_national_team(data):
    first_filter = filter_players_by_games_played(data)
    sorted_players = sort_players_by_position(first_filter)

    result = {}
    for position in sorted_players:
        result[position] = extract_position_data(sorted_players, position)

    return result