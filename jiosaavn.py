import requests
import endpoints
import helper
import json
from traceback import print_exc
import re
import os

def format_duration(duration_seconds):
    if not duration_seconds:
        return "0:00"
    try:
        total_seconds = int(duration_seconds)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    except:
        return "0:00"

def map_jiosaavn_to_song(track):
    image = track.get('image') or track.get('image_url') or ""
    if image and not image.startswith('http'):
        image = f"https://c.saavncdn.com/{image.lstrip('/')}"
    if not image:
        image = "https://via.placeholder.com/500"
        
    if isinstance(image, str):
        image = image.replace('150x150', '500x500').replace('50x50', '500x500')
    
    media_url = track.get('media_url') or track.get('url') or track.get('preview_url') or ""
    if media_url and not media_url.startswith('http'):
        media_url = f"https://aac.saavncdn.com/{media_url.lstrip('/')}"
    
    # Route through proxy if it's a saavncdn link to bypass CORS/Mixed Content
    if media_url and 'saavncdn.com' in media_url:
        if not media_url.startswith('/api/audio-proxy'):
            media_url = f"/api/audio-proxy?url={media_url}"

    return {
        "id": str(track.get('id', 'unknown')),
        "title": track.get('song') or track.get('title') or 'Unknown',
        "artist": track.get('singers') or track.get('primary_artists') or 'Unknown Artist',
        "album": track.get('album') or 'Unknown Album',
        "duration": format_duration(track.get('duration')),
        "coverUrl": image,
        "preview": media_url,
        "isFavorite": False,
        "source": "jiosaavn"
    }


def search_for_song(query, lyrics, songdata):
    if query.startswith('http') and 'saavn.com' in query:
        id = get_song_id(query)
        return get_song(id, lyrics)

    search_base_url = endpoints.search_base_url+query
    response = requests.get(search_base_url).text.encode().decode('unicode-escape')
    pattern = r'\(From "([^"]+)"\)'
    response = json.loads(re.sub(pattern, r"(From '\1')", response))
    song_response = response['songs']['data']
    if not songdata:
        return [map_jiosaavn_to_song(s) for s in song_response]
    songs = []
    for song in song_response:
        id = song['id']
        song_data = get_song(id, lyrics)
        if song_data:
            songs.append(map_jiosaavn_to_song(song_data))
    return songs


def get_song(id, lyrics):
    try:
        song_details_base_url = endpoints.song_details_base_url+id
        song_response = requests.get(
            song_details_base_url).text.encode().decode('unicode-escape')
        song_response = json.loads(song_response)
        song_data = helper.format_song(song_response[id], lyrics)
        if song_data:
            return song_data
    except:
        return None


def get_song_id(url):
    res = requests.get(url, data=[('bitrate', '320')])
    try:
        return(res.text.split('"pid":"'))[1].split('","')[0]
    except IndexError:
        return res.text.split('"song":{"type":"')[1].split('","image":')[0].split('"id":"')[-1]


def get_album(album_id, lyrics):
    songs_json = []
    try:
        response = requests.get(endpoints.album_details_base_url+album_id)
        if response.status_code == 200:
            songs_json = response.text.encode().decode('unicode-escape')
            songs_json = json.loads(songs_json)
            return helper.format_album(songs_json, lyrics)
    except Exception as e:
        print(e)
        return None


def get_album_id(input_url):
    res = requests.get(input_url)
    try:
        return res.text.split('"album_id":"')[1].split('"')[0]
    except IndexError:
        return res.text.split('"page_id","')[1].split('","')[0]


def get_playlist(listId, lyrics):
    try:
        response = requests.get(endpoints.playlist_details_base_url+listId)
        if response.status_code == 200:
            songs_json = response.text.encode().decode('unicode-escape')
            songs_json = json.loads(songs_json)
            return helper.format_playlist(songs_json, lyrics)
        return None
    except Exception:
        print_exc()
        return None


def get_playlist_id(input_url):
    res = requests.get(input_url).text
    try:
        return res.split('"type":"playlist","id":"')[1].split('"')[0]
    except IndexError:
        return res.split('"page_id","')[1].split('","')[0]


def get_lyrics(id):
    url = endpoints.lyrics_base_url+id
    lyrics_json = requests.get(url).text
    lyrics_text = json.loads(lyrics_json)
    return lyrics_text['lyrics']
