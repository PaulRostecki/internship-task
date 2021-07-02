import flask
import json
from flask_accept import accept
from dict2xml import dict2xml

app = flask.Flask(__name__)

def handle_ip():
    user_ip = flask.request.remote_addr
    with open("iplist.json", "r+") as file:
        data = json.load(file)
        data['ip'].append(user_ip)
        file.seek(0)
        json.dump(data, file)
    return user_ip


@app.route('/', methods=['GET'])
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
def html():

    iplist = []

    with open("iplist.json", "r") as file:
        data = json.load(file)
        iplist = data['ip']

    return str(iplist)

app.run(host='0.0.0.0')
