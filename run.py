import flask
import json

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def get_ip():
    user_ip = flask.request.remote_addr

    with open("iplist.json", "r+") as file:
        data = json.load(file)
        data['ip'].append(user_ip)
        file.seek(0)
        json.dump(data, file)

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

app.run(host='0.0.0.0')
