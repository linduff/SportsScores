from flask import Flask, render_template
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.route('/')
def scores():
    url = 'http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard'
    response = urlopen(url)
    data_json = json.loads(response.read())
    formattedData = formatJsonMLB(data_json)
    return render_template('sportsScores.html', data=formattedData)

def formatJsonMLB(data_json):
    data = []
    for event in data_json['events']:
        homeData = event['competitions'][0]['competitors'][0] if event['competitions'][0]['competitors'][0]['homeAway'] == 'home' else event['competitions'][0]['competitors'][1]
        awayData = event['competitions'][0]['competitors'][0] if event['competitions'][0]['competitors'][0]['homeAway'] == 'away' else event['competitions'][0]['competitors'][1]
        data.append({'homeData': homeData, 'awayData': awayData})
    return data