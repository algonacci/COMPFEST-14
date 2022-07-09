from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
  return 'Hello World!'

@app.route('/json')
def json():
    json = {
        'message': 'Hello World!'
    }
    return jsonify(json)

if __name__ == '__main__':
  app.run()
