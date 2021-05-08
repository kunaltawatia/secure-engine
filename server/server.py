from execution import run
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(
  __name__,
  static_url_path='',
  static_folder='build')
CORS(app)

@app.route('/', methods=['GET'])
def entry():
  return app.send_static_file('index.html')

@app.route('/', methods=['POST'])
def submit():
  if not request.json or not 'code' in request.json:
    return 'Code not found'
  code = request.json['code']
  inp = request.json['input'] if 'input' in request.json else ''
  return run(code, inp)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, threaded=False, processes=1)