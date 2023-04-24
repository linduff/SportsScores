from flask import Flask, render_template
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.route('/')
def scores():
    url = 'http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard'
    response = urlopen(url)
    data_json = json.loads(response.read())
    return render_template('sportsScores.html', data=data_json)