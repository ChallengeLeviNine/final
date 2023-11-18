import csv
import json
from flask import Flask, jsonify
from loadAll import loadAllData
from filter import *

app = Flask(__name__)
player_data = None

# loading data from csv
def load_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)

        #skipping header
        next(csv_reader)

        for row in csv_reader:
            data.append(row)
    return data

# API endpoint
@app.route('/stats/', methods=['GET'])
def get_stats():
    global player_data
    if player_data is None:
        player_data = load_data('L9HackathonPlayersInput.csv')

    player_stats = loadAllData(player_data)
    #print("ovo sam dobio kao resenje ", player_stats)
    new = get_candidates_for_national_team(player_stats)

    # Assuming player_stats is a list of dictionaries
    response = jsonify(new)
    
    return response  # Return the response object directly

if __name__ == '__main__':
    app.run(debug=True)