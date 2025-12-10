import flask
from flask_cors import CORS
import youtubesearchpython as yts

app = flask.Flask(__name__, static_folder="frontend")
CORS(app)

def search_youtube_videos(query, limit=10):
    search = yts.VideosSearch(query, limit=limit)
    results = search.result()
    videos = []
    for video in results['result']:
        videos.append({
            "title": video['title'],
            "id": video['id'],
            "channel": video['channel']['name'],
            "description": video.get('descriptionSnippet', ''),
            "thumbnail": video['thumbnails'][0]['url'],
            "duration": video['duration'],
            "views": video['viewCount']['text'],
            "link": f"https://www.youtube.com/watch?v={video['id']}"
        })
    return videos

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
    results = search_youtube_videos(query)
    return flask.jsonify({"results": results})
if __name__ == '__main__':
    app.run(debug=True, port=1318)