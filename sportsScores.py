from flask import Flask, render_template
from urllib.request import urlopen
import json
import datetime

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
        data.append(formatGameData(event))
    return data

def formatGameData(event):
    homeData = event['competitions'][0]['competitors'][0] if event['competitions'][0]['competitors'][0]['homeAway'] == 'home' else event['competitions'][0]['competitors'][1]
    awayData = event['competitions'][0]['competitors'][0] if event['competitions'][0]['competitors'][0]['homeAway'] == 'away' else event['competitions'][0]['competitors'][1]
    return {
        'status': event['status']['type']['name'],
        'detail': getDetail(event['status']['type']['name'], event['status']['type']['detail']),
        'shortDetail': event['status']['type']['shortDetail'],
        'homeData': {
            'teamLocation': homeData['team']['location'],
            'teamName': homeData['team']['name'],
            'abbreviation': homeData['team']['abbreviation'],
            'record': getRecord(homeData['records']),
            'logo': homeData['team']['logo'],
            'runs': homeData['score'],
            'hits': homeData['hits'],
            'erors': homeData['errors'],
            'linescore': getLineScore(homeData)
        },
        'awayData': {
            'teamLocation': awayData['team']['location'],
            'teamName': awayData['team']['name'],
            'abbreviation': awayData['team']['abbreviation'],
            'record': getRecord(awayData['records']),
            'logo': awayData['team']['logo'],
            'runs': awayData['score'],
            'hits': awayData['hits'],
            'erors': awayData['errors'],
            'linescore': getLineScore(awayData)
        }
    }

def getDetail(status, dateTimeString):
    if status == 'STATUS_SCHEDULED':
        splitString = dateTimeString.split()
        for i in range(len(splitString)):
            if ':' in splitString[i]:
                dateTimeString = splitString[i] + ' ' + splitString[i+1]
    return dateTimeString

def getRecord(records):
    rec = '0-0'
    for record in records:
        if record['name'] == 'overall':
            rec = record['summary']
    return rec

def getLineScore(teamData):
    linescore = ['-','-','-','-','-','-','-','-','-']
    if 'linescores' in teamData:
        for inning in range(len(teamData['linescores'])):
            linescore[inning] = teamData['linescores'][inning]['value']
    return linescore
