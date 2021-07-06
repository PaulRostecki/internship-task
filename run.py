import flask
import json
from flask_accept import accept
import yaml
import os
import pymongo

app = flask.Flask(__name__)

PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
DB_USERNAME = os.environ.get('MONGODB_USER', 'admin')
DB_PASSWORD = os.environ.get('MONGODB_PASSWORD', 'admin')
DB_NAME = os.environ.get('MONGODB_DATABASE', 'sampledb')
DB_HOST = os.environ.get('MONGODB_SERVICE_HOST', '0.0.0.0')
DB_PORT = os.environ.get('MONGODB_SERVICE_PORT', 27017)

uri = "mongodb://" + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT + '/' + DB_NAME

client = pymongo.MongoClient(uri)
db = client[DB_NAME]
col = db["ip"]

def handle_ip():
    user_ip = flask.request.remote_addr
    dict = {'ip': user_ip}
    x = col.insert_one(dict)
    return user_ip

def fetch_ip():
    tab = []
    for x in col.find({},{ "_id": 0, "ip": 1}):
        tab.append(x['ip'])
    return tab

@app.route('/')
def hello():
    return "Welcome to Get IP page!"

@app.route('/ip', methods=['GET'])
@accept('text/html')
def get_ip():
    user_ip = handle_ip()
    return flask.render_template_string('''
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <title>What is my IP?</title>
      </head>
      <body>
        {{ ip }}
      </body>
    </html>
    ''', ip=user_ip)

@get_ip.support('text/plain')
def get_ip_text():
    user_ip = handle_ip()
    return user_ip

@get_ip.support('application/json')
def get_ip_json():
    user_ip = handle_ip()
    return flask.jsonify(ip=user_ip)

@get_ip.support('text/yaml')
def get_ip_xml():
    user_ip = handle_ip()
    return yaml.dump({'ip': user_ip})

@app.route('/iplist', methods=['GET'])
@accept('text/html')
def iplist():
    list = fetch_ip()
    return flask.render_template_string('''
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <title>IP List</title>
      </head>
      <body>
        {{ list }}
      </body>
    </html>
    ''', list=list)

@iplist.support('text/plain')
def iplist_text():
    list = fetch_ip()
    return str(list)

@iplist.support('application/json')
def iplist_json():
    list = fetch_ip()
    return flask.jsonify(ip=list)

@iplist.support('text/yaml')
def iplist_xml():
    list = fetch_ip()
    return yaml.dump({'ip': list})

#added, because openshift probe has no option to set 'Accept' header and always returns 406 when checking /iplist
@app.route('/iplist/probe', methods=['GET'])
def iplist_probe():
    list = fetch_ip()
    return str(fetch_ip)

app.run(host='0.0.0.0', port=PORT)
