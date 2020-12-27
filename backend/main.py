from flask import Flask, request
from os.path import abspath, dirname
from datetime import datetime
from shutil import copy
from zipfile import ZipFile as TheJarGuy
import os, json, random
app = Flask(__name__)

OSR = random.SystemRandom()

activeSessions = []
newSessions = []

def invalidateSessions():
    global newSessions
    for session in newSessions:
        if (datetime.now() - session['gentime']).seconds > 5:
            deleteJAR(session['download'])
            newSessions.remove(session)

def activateSession(sessionID):
    invalidateSessions()
    global newSessions
    global activeSessions
    for session in newSessions:
        if str(session['id']) == sessionID:
            activeSessions.append(session)
            deleteJAR(session['download'])
            newSessions.remove(session)
    return 'OK'

def generateSessionID():
    global OSR
    return OSR.randint(1, 1000)
# The real session ID system obviously won't give random numbers, this is for prototyping purposes.
# Also we are assuming we won't get the same ID twice. It's a 0.1% chance :)

def generateJSON(id):
    data = {
        "sessionID": id
    }
    with open(os.path.join(dirname(abspath(__file__)), 'jars', 'temp', f'{id}.json'), 'x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return os.path.join(dirname(abspath(__file__)), 'jars', 'temp', f'{id}.json')

def generateJAR(id):
    copy(os.path.join(dirname(abspath(__file__)), 'assets', 'ref.jar'), os.path.join(dirname(abspath(__file__)), 'jars', f'{id}.jar'))
    with TheJarGuy(os.path.join(dirname(abspath(__file__)), 'jars', f'{id}.jar'), 'a') as newJAR:
        newJAR.write(generateJSON(id), 'sessionID.json')
    newJAR.close()
    os.remove(os.path.join(dirname(abspath(__file__)), 'jars', 'temp', f'{id}.json'))
    return os.path.join(dirname(abspath(__file__)), 'jars', f'{id}.jar')
    # This would normally give the a URL to the jar download.

def deleteJAR(jarfile):
    os.remove(jarfile)

def createSession(reqform):
    global newSessions
    ID = generateSessionID()
    session = {
        "id": ID,
        "username": reqform['username'],
        "gentime": datetime.now(),
        "download": generateJAR(ID)
    }
    newSessions.append(session)
    return session

@app.route('/launcher', methods=['POST'])
def launcher():
    return createSession(request.form)

@app.route('/instance', methods=['POST'])
def instance():
    return activateSession(request.form.getlist('id')[0])

# http://localhost:5000/debug will return a page with activated sessions' info
@app.route('/debug', methods=['GET'])
def debug():
    global activeSessions
    page = ''
    for session in activeSessions:
        page += f'Session {activeSessions.index(session) + 1}/{len(activeSessions)} </br>'
        page += f'Username: ' + session['username'] + '</br>'
        page += f'Session ID: ' + str(session['id']) + '</br>'
        page += f'Generation Time: ' + str(session['gentime']) + '</br> </br>'
    return page

if __name__ == "__main__":
    app.run(debug=True)