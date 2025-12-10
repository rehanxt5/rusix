from youtubesearchpython import VideosSearch

# Search for videos
search = VideosSearch('still be friends', limit=10)
results = search.result()

# Access the results
for video in results['result']:
    print(f"Title: {video['title']}")
    print(f"Video ID: {video['id']}")
    print(f"Channel: {video['channel']['name']}")
    print(f"Description: {video['descriptionSnippet']}")
    print(f"Thumbnail: {video['thumbnails'][0]['url']}")
    print(f"Duration: {video['duration']}")
    print(f"Views: {video['viewCount']['text']}")
    print(f"Link: https://www.youtube.com/watch?v={video['id']}")
    print("-" * 50)
