from flask import Flask, render_template, request, redirect
import time
from flask import jsonify, json
import saavn
from traceback import print_exc
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'thankyoutonystark#weloveyou3000'
CORS(app)


@app.route('/')
def home():
    return redirect("https://cyberboysumanjay.github.io/JioSaavnAPI/")


@app.route('/result/', methods=['GET', 'POST'])
def result():
    lyrics = False
    false = False
    true = True
    query = request.args.get('query')
    lyrics_ = request.args.get('lyrics')
    if lyrics_ and lyrics_.lower()!='false':
        lyrics = True

    if 'saavn' not in query:
        return jsonify(saavn.search_from_query(query))
    print("Checking Lyrics Tag:",lyrics)
    try:
        if '/song/' in query:
            print("Song")
            song = saavn.get_song_id(query)
            song = (saavn.search_from_song_id(song))
            if lyrics:
                if song['has_lyrics']:
                    song['lyrics'] = saavn.get_lyrics(song['perma_url'])
                else:
                    song['lyrics'] = None
            song['status'] = True
            song['media_url'] = saavn.check_media_url(song['media_url'])
            return jsonify(song)
            '''
            elif '/search/' in query:
                songs = saavn.get_songs(query)
                for song in songs:
                    song['image_url'] = saavn.fix_image_url(song['image_url'])
                    song['title'] = saavn.fix_title(song['title'])
                    song['url'] = saavn.decrypt_url(song['url'])
                    song['album'] = saavn.fix_title(song['album'])
                    if lyrics:
                        song['lyrics'] = saavn.get_lyrics(song['tiny_url'])
                return jsonify(songs)
            '''
        elif '/album/' in query:
            print("Album")
            id = saavn.AlbumId(query)
            songs = saavn.getAlbum(id)
            for song in songs['songs']:
                song['media_url'] = saavn.check_media_url(song['media_url'])
                if lyrics:
                    if song['has_lyrics']:
                        song['lyrics'] = saavn.get_lyrics(song['perma_url'])
                    else:
                        song['lyrics'] = None
            songs['status'] = True
            return jsonify(songs)
        elif '/playlist/' or '/featured/' in query:
            print("Playlist")
            id = saavn.getListId(query)
            songs = saavn.getPlayList(id)
            for song in songs['songs']:
                song['media_url'] = saavn.check_media_url(song['media_url'])
                if lyrics:
                    if song['has_lyrics']:
                        song['lyrics'] = saavn.get_lyrics(song['perma_url'])
                    else:
                        song['lyrics'] = None
            songs['status'] = True
            return jsonify(songs)
    except Exception as e:
        print_exc()
        error = {
            "status": True,
            "error":str(e)
        }
        return jsonify(error)
    return None


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000, use_reloader=True, threaded=True)
