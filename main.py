import flask
from flask_cors import CORS
import youtubesearchpython as yts
import os

import yt_dlp

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

def download_youtube_audio(video_url):
    os.makedirs('userData/audio', exist_ok=True)
    output_path = os.path.join('userData', 'audio')
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

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

@app.route('/downloadYoutube', methods=['POST'])
def download_youtube():
    data = flask.request.get_json()
    video_id = data.get('videoId', '')
    print("Video ID to download:", video_id)
    if video_id:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print("Constructed video URL:", video_url)
        download_youtube_audio(video_url)
        return flask.jsonify({"status": "success", "message": "Download started"})
    else:
        return flask.jsonify({"status": "error", "message": "No video ID provided"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=1318)