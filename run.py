import flask
import json
from flask_accept import accept
from dict2xml import dict2xml
import os
import pymongo

app = flask.Flask(__name__)

PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
DB_USERNAME = os.environ.get('MONGODB_USER', 'admin')
DB_PASSWORD = os.environ.get('MONGODB_ADMIN_PASSWORD', 'admin')
DB_NAME = os.environ.get('MONGODB_DATABASE', 'sampledb')

client = pymongo.MongoClient(host=localhost,
                                port=27017,
                                username=DB_USERNAME,
                                password=DB_PASSWORD)
db = client["database"]
col = db["ip"]

def handle_ip():
    user_ip = flask.request.remote_addr
    dict = {'ip': user_ip}
    x = col.insert_one(dict)
    return user_ip

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

@get_ip.support('application/xml')
def get_ip_xml():
    user_ip = handle_ip()
    return dict2xml({'ip': user_ip})

@app.route('/iplist', methods=['GET'])
def iplist():
    tab = []
    for x in col.find({},{ "_id": 0, "ip": 1}):
        tab.append(x['ip'])

    return flask.jsonify(iplist)

app.run(host='0.0.0.0', port=PORT)
