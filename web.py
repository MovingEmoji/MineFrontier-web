from bottle import Bottle, run, route, template, request, os, static_file
from mojang import API
from paste import httpserver as web

app = Bottle()

@app.route('/')
def home():
    return static_file('home.html', root="./")
@app.route('/news')
def news():
    return static_file('news.html', root="./")
@app.route('/staff')
def staff():
    return static_file('staff.html', root="./")
@app.route('/player')
def player():
    return static_file('player.html', root="./")
@app.route('/rule')
def rule():
    return static_file('rule.html', root="./")
@app.route('/resouces/<filename:path>')
def static(filename):
    return static_file(filename, root="./resouces")
@app.route('/news/<filename:path>')
def news(filename):
    if '/' in filename:
        return static_file(filename, root="./")
    else:
        return static_file(filename + '.html', root="./")
@app.route('/player/<name>')
def convert(name):
    if '/' in name:
        return static_file(name, root="./")
    else:
        uuid = API.get_uuid(name)
        if not uuid:
            uuid = API.get_profile(name).id
            if not uuid:
                print(name + 'does not found.')
            else:
                uuid = uuid[0:8] + '-' + uuid[8:12] + '-' + uuid[12:16] + '-' + uuid[16:20] + '-' + uuid[20:32]
        else:
            uuid = uuid[0:8] + '-' + uuid[8:12] + '-' + uuid[12:16] + '-' + uuid[16:20] + '-' + uuid[20:32]
        name=API.get_profile(uuid).name
        jobfile = open("../PlayerData/" + uuid + "/lastjob.yml", "r")
        jobtext = jobfile.readline()
        jobfile.closed
        jobtext = jobtext.replace("\n","")
        parameter = open("../PlayerData/" + uuid + "/" + jobtext + ".yml")
        prs = parameter.readlines()
        parameter.closed
        level= prs.pop(0).replace("level: ","")
        xp= prs.pop(0).replace("xp: ","")
        meele = prs.pop(1).replace("meeledamage: ","")
        protection = prs.pop(1).replace("protection: ","")
        magic = prs.pop(1).replace("magicdamage: ","")
        mp = prs.pop(1).replace("mp: ","")
        hp = prs.pop(1).replace("health: ","")
        return template('playerpage', mcid=name, id=uuid, job=jobtext, levelweb=level, xpweb=xp, meeleweb=meele, protectionweb=protection, magicweb=magic, mpweb=mp, hpweb=hp)
web.serve(app,host='192.168.1.16', port=5400, daemon_threads=False, threadpool_workers=25, use_threadpool=True)