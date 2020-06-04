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
    data = ''
    lyrics = False
    query = request.args.get('query')
    lyrics_ = request.args.get('lyrics')
    if lyrics_ and lyrics_.lower()!='false':
        lyrics = True

    if not query.startswith('https://www.jiosaavn.com'):
        query = "https://www.jiosaavn.com/search/"+query

    try:
        print("Query received: ", query)
        if '/song/' in query:
            print("Song")
            song = saavn.get_songs(query)[0]
            song['image_url'] = saavn.fix_image_url(song['image_url'])
            song['title'] = saavn.fix_title(song['title'])
            song['url'] = saavn.decrypt_url(song['url'])
            song['album'] = saavn.fix_title(song['album'])
            if lyrics:
                song['lyrics'] = saavn.get_lyrics(query)
            return jsonify(song)
        elif '/search/' in query:
            print("Text Query Detected")
            songs = saavn.get_songs(query)
            for song in songs:
                song['image_url'] = saavn.fix_image_url(song['image_url'])
                song['title'] = saavn.fix_title(song['title'])
                song['url'] = saavn.decrypt_url(song['url'])
                song['album'] = saavn.fix_title(song['album'])
                if lyrics:
                    song['lyrics'] = saavn.get_lyrics(song['tiny_url'])
            return jsonify(songs)
        elif '/album/' in query:
            print("Album")
            id = saavn.AlbumId(query)
            songs = saavn.getAlbum(id)
            for song in songs["songs"]:
                song['image'] = saavn.fix_image_url(song['image'])
                song['song'] = saavn.fix_title(song['song'])
                song['album'] = saavn.fix_title(song['album'])
                if lyrics:
                    song['lyrics'] = saavn.get_lyrics(song['perma_url'])
                song['encrypted_media_path'] = saavn.decrypt_url(
                    song['encrypted_media_path'])
            return jsonify(songs)
        elif '/playlist/' or '/featured/' in query:
            print("Playlist")
            id = saavn.getListId(query)
            songs = saavn.getPlayList(id)
            for song in songs['songs']:
                song['image'] = saavn.fix_image_url(song['image'])
                song['song'] = saavn.fix_title(song['song'])
                if lyrics:
                    song['lyrics'] = saavn.get_lyrics(song['perma_url'])
                song['encrypted_media_path'] = saavn.decrypt_url(
                    song['encrypted_media_path'])
            return jsonify(songs)
        raise AssertionError
    except Exception as e:
        errors = []
        print_exc()
        error = {
            "status": str(e)
        }
        errors.append(error)
        return jsonify(errors)
    return data


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000, use_reloader=True, threaded=True)
