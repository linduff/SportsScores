from flask import Flask, render_template
from urllib.request import urlopen
import json
import datetime

app = Flask(__name__)

@app.route('/')
def scores():
    mlb_url = 'http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates=' + datetime.datetime.now().strftime("%Y%m%d")
    mlb_response = urlopen(mlb_url)
    mlb_data_json = json.loads(mlb_response.read())
    formattedMLBData = formatJson(mlb_data_json, 'MLB')

    nba_url = 'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20230501'
    nba_response = urlopen(nba_url)
    nba_data_json = json.loads(nba_response.read())
    formattedNBAData = formatJson(nba_data_json, 'NBA')

    return render_template('sportsScores.html', mlb_data=formattedMLBData, nba_data=formattedNBAData)

def formatJson(data_json, sport):
    data = []
    for event in data_json['events']:
        data.append(formatGameData(event, sport))
    return data

def formatGameData(event, sport):
    homeData = event['competitions'][0]['competitors'][0] if event['competitions'][0]['competitors'][0]['homeAway'] == 'home' else event['competitions'][0]['competitors'][1]
    awayData = event['competitions'][0]['competitors'][0] if event['competitions'][0]['competitors'][0]['homeAway'] == 'away' else event['competitions'][0]['competitors'][1]
    gameData = {
        'id': event['id'],
        'status': event['status']['type']['name'],
        'detail': getDetail(event['status']['type']['name'], event['status']['type']['detail']),
        'shortDetail': event['status']['type']['shortDetail'],
        'homeData': {
            'teamLocation': homeData['team']['location'],
            'teamName': homeData['team']['name'],
            'abbreviation': homeData['team']['abbreviation'],
            'record': getRecord(homeData['records']),
            'logo': homeData['team']['logo'],
            'score': homeData['score'],
            'linescore': getLineScore(event, homeData, sport)
        },
        'awayData': {
            'teamLocation': awayData['team']['location'],
            'teamName': awayData['team']['name'],
            'abbreviation': awayData['team']['abbreviation'],
            'record': getRecord(awayData['records']),
            'logo': awayData['team']['logo'],
            'score': awayData['score'],
            'linescore': getLineScore(event, awayData, sport)
        }
    }

    if sport == 'MLB':
        gameData['homeData']['hits'] = homeData['hits']
        gameData['homeData']['errors'] = homeData['errors']
        gameData['awayData']['hits'] = awayData['hits']
        gameData['awayData']['errors'] = awayData['errors']
    return gameData

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

def getLineScore(event, teamData, sport):
    if sport == 'MLB':
        linescore = ['-','-','-','-','-','-','-','-','-']
    elif sport == 'NBA':
        linescore = ['-','-','-','-']
    if 'linescores' in teamData:
        for period in range(len(teamData['linescores'])):
            linescore[period] = int(teamData['linescores'][period]['value'])
        if event['status']['type']['name'] == 'STATUS_FINAL' and len(teamData['linescores']) == 8:
            linescore[-1] = 'X'
    return linescore
