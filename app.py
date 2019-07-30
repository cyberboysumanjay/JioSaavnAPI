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

    try:
        data=saavn.get_songs(query)
        for song in data:
            song['image_url']=saavn.fix_image_url(song['image_url'])
            song['title']=saavn.fix_title(song['title'])
            song['url']=saavn.decrypt_url(song['url'])
        if len(data)>0:
            if '/song/' in query:
                return jsonify(data[0])
            else:
                return jsonify(data)
        raise AssertionError
    except Exception as e:
        errors=[]
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
