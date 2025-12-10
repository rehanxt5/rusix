import flask
from flask_cors import CORS

app = flask.Flask(__name__, static_folder="frontend")
CORS(app)


@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/health')
def health():
    return "OK"
@app.route('/searchYoutube', methods=['POST'])
def search_youtube():
    print("Route hit!")
    data = flask.request.get_json()
    print("Received data:", data)
    query = data.get('query', '')
    print("Query:", query)
    return flask.jsonify({"results": []})
if __name__ == '__main__':
    app.run(debug=True, port=1318)