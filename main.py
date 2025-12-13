import flask
from flask_cors import CORS
import youtubesearchpython as yts
import os
from PIL import Image
import io
import yt_dlp
import rusix_modules.config_db as config_db
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
    """Download YouTube audio and thumbnail, return metadata"""
    os.makedirs('userData/audio', exist_ok=True)
    os.makedirs('userData/thumbnails', exist_ok=True)
    
    output_path = os.path.join('userData', 'audio')
    
    # Configure yt-dlp to download audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
    }

    # Extract video info and download audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        
        # Extract metadata
        title = info.get('title', 'unknown')
        duration = info.get('duration', 0)  # in seconds
        artist = info.get('uploader', 'Unknown Artist')
        thumbnail_url = info.get('thumbnail')
        
        # Construct audio path
        audio_filename = ydl.prepare_filename(info)
        song_path = os.path.splitext(audio_filename)[0] + '.mp3'
    
    # Download and process thumbnail
    thumbnail_path = None
    if thumbnail_url:
        try:
            import urllib.request
            thumbnail_filename = f"{title}_square.jpg"
            thumbnail_path = os.path.join('userData', 'thumbnails', thumbnail_filename)
            
            # Download thumbnail image
            urllib.request.urlretrieve(thumbnail_url, thumbnail_path)
            
            # Crop to square (center crop)
            img = Image.open(thumbnail_path)
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) // 2
            top = (height - min_dim) // 2
            right = left + min_dim
            bottom = top + min_dim
            
            square_img = img.crop((left, top, right, bottom))
            square_img.save(thumbnail_path)
        except Exception as e:
            print(f"Error processing thumbnail: {e}")
            thumbnail_path = None
    
    # Save to Database 
    config_db.add_song_to_library(title=title, artist=artist, album='', duration=duration, url=video_url, thumbnail=thumbnail_path)
   
    

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
        metadata = download_youtube_audio(video_url)
        return flask.jsonify({
            "status": "success", 
            "message": "Download completed",
            "data": metadata
        })
    else:
        return flask.jsonify({"status": "error", "message": "No video ID provided"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=1318)