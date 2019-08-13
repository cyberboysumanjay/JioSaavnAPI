from flask import Flask, render_template,request
import time
from flask import  jsonify,json
import saavn
from traceback import print_exc
app = Flask(__name__)
app.secret_key = 'thankyoutonystark#weloveyou3000'

@app.route('/')
def home():
   return "Thanks for testing Saavn API. To get started head up to my GitHub for documentation."

@app.route('/result/', methods=['GET', 'POST'])
def result():
    data=''
    query=request.args.get('query')
    #link='https://www.jiosaavn.com/song/hawa-banke/JSw6aUYIRX8'
    if not query.startswith('http'):
        query = "https://www.jiosaavn.com/search/"+query
    proxies=saavn.fate_proxy()
    try:
        if '/song/' in query:
            song=saavn.get_songs(query,proxies)[0]
            song['image_url']=saavn.fix_image_url(song['image_url'])
            song['title']=saavn.fix_title(song['title'])
            song['url']=saavn.decrypt_url(song['url'])
            return jsonify(song)
        elif '/album/' in query:
            id=saavn.AlbumId(query,proxies)
            songs=saavn.getAlbum(id,proxies)
            for song in songs["songs"]:
                song['image']=saavn.fix_image_url(song['image'])
                song['song']=saavn.fix_title(song['song'])
                song['encrypted_media_path']=saavn.decrypt_url(song['encrypted_media_path'])
            return jsonify(songs)
        elif '/playlist/' or '/featured/' in query:
            id=saavn.getListId(query,proxies)
            songs=saavn.getPlayList(id,proxies)
            for song in songs["songs"]:
                song['image']=saavn.fix_image_url(song['image'])
                song['song']=saavn.fix_title(song['song'])
                song['encrypted_media_path']=saavn.decrypt_url(song['encrypted_media_path'])
            return jsonify(songs)
        else:
            songs=saavn.get_songs(query,proxies)
            for song in songs:
                song['image_url']=saavn.fix_image_url(song['image_url'])
                song['title']=saavn.fix_title(song['title'])
                song['url']=saavn.decrypt_url(song['url'])
            return jsonify(songs)
        raise AssertionError
    except Exception as e:
        errors=[]
        print_exc()
        error = {"album": "NULL",
                "album_url": "NULL",
                "autoplay": "NULL",
                "duration": "NULL",
                "e_songid": "NULL",
                "has_rbt": "NULL",
                "image_url":"NULL",
                "label": "NULL",
                "label_url":"NULL",
                "language": "NULL",
                "liked": "NULL",
                "map":"NULL",
                "music": "NULL",
                "origin": "NULL",
                "origin_val": "NULL",
                "page": "NULL",
                "pass_album_ctx": "NULL",
                "perma_url": "NULL",
                "publish_to_fb": "NULL",
                "singers": "NULL",
                "songid": "NULL",
                "starred":"NULL",
                "starring": "NULL",
                "streaming_source":"NULL",
                "tiny_url": "NULL",
                "title": "NULL",
                "twitter_url": "NULL",
                "url": "NULL",
                "year": "NULL",
                "status":str(e)
            }
        errors.append(error)
        return jsonify(errors)
    return data

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000,use_reloader=True)
