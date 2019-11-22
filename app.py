from flask import Flask, render_template,request,redirect
import time
from flask import  jsonify,json
import saavn
from traceback import print_exc
app = Flask(__name__)
app.secret_key = 'thankyoutonystark#weloveyou3000'

@app.route('/')
def home():
   return redirect("https://cyberboysumanjay.github.io/JioSaavnAPI/")

@app.route('/result/', methods=['GET', 'POST'])
def result():
    data=''
    query=request.args.get('query')
    proxies=saavn.fate_proxy()
    if not query.startswith('https://www.jiosaavn.com'):
        query = "https://www.jiosaavn.com/search/"+query

    try:
        print("All is well with query",query)
        if '/song/' in query:
            print("Song")
            song=saavn.get_songs(query,proxies)[0]
            song['image_url']=saavn.fix_image_url(song['image_url'])
            song['title']=saavn.fix_title(song['title'])
            song['url']=saavn.decrypt_url(song['url'])
            song['album']=saavn.fix_title(song['album'])
            song['lyrics']=saavn.get_lyrics(query)
            return jsonify(song)
        elif '/search/' in query:
            print("Text Query Detected")
            songs=saavn.get_songs(query,proxies)
            for song in songs:
                song['image_url']=saavn.fix_image_url(song['image_url'])
                song['title']=saavn.fix_title(song['title'])
                song['url']=saavn.decrypt_url(song['url'])
                song['album']=saavn.fix_title(song['album'])
                song['lyrics']=saavn.get_lyrics(song['tiny_url'])
            return jsonify(songs)
        elif '/album/' in query:
            print("Album")
            id=saavn.AlbumId(query,proxies)
            songs=saavn.getAlbum(id,proxies)
            for song in songs["songs"]:
                song['image']=saavn.fix_image_url(song['image'])
                song['song']=saavn.fix_title(song['song'])
                song['album']=saavn.fix_title(song['album'])
                song['lyrics']=saavn.get_lyrics(song['perma_url'])
                song['encrypted_media_path']=saavn.decrypt_url(song['encrypted_media_path'])
            return jsonify(songs)
        elif '/playlist/' or '/featured/' in query:
            print("Playlist")
            id=saavn.getListId(query,proxies)
            songs=saavn.getPlayList(id,proxies)
            for song in songs['songs']:
                song['image']=saavn.fix_image_url(song['image'])
                song['song']=saavn.fix_title(song['song'])
                song['lyrics']=saavn.get_lyrics(song['perma_url'])
                song['encrypted_media_path']=saavn.decrypt_url(song['encrypted_media_path'])
            return jsonify(songs)
        raise AssertionError
    except Exception as e:
        errors=[]
        print_exc()
        error = {
                "status":str(e)
            }
        errors.append(error)
        return jsonify(errors)
    return data

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000,use_reloader=True,threaded = True)
