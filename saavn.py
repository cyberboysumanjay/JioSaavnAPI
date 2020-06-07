import urllib3
import re
from traceback import print_exc
import ast
import json
from pyDes import *
import os
import base64
from bs4 import BeautifulSoup
import requests


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0",
                 pad=None, padmode=PAD_PKCS5)
base_url = 'http://h.saavncdn.com'
json_decoder = json.JSONDecoder()
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
}


def get_songs(query):
    if not query.startswith('https://www.jiosaavn.com'):
        url = "https://www.jiosaavn.com/search/"+query
    else:
        url = query
    songs = []
    try:
        res = requests.get(url, headers=headers, data=[('bitrate', '320')])
        soup = BeautifulSoup(res.text, "lxml")
        all_song_divs = soup.find_all('div', {"class": "hide song-json"})
        for i in all_song_divs:
            try:
                try:
                    song_info = json.loads(i.text)
                    songs.append(song_info)
                except:
                    esc_text = re.sub(r'.\(\bFrom .*?"\)', "", str(i.text))
                    try:
                        song_info = json_decoder.decode(esc_text)
                        songs.append(song_info)
                    except:
                        try:
                            song_info = json.loads(esc_text)
                            songs.append(song_info)
                        except:
                            print(esc_text)

            except Exception as e:
                print_exc()
                continue
        if len(songs) > 0:
            return songs
    except Exception as e:
        print_exc()
    return songs


def getAlbum(albumId):
    songs_json = []
    try:
        response = requests.get(
            'https://www.jiosaavn.com/api.php?_format=json&__call=content.getAlbumDetails&albumid={0}'.format(albumId), verify=False)
        if response.status_code == 200:
            songs_json = list(filter(lambda x: x.startswith(
                "{"), response.text.splitlines()))[0]
            songs_json = json.loads(songs_json)
            return songs_json
    except Exception as e:
        print_exc()
        return None


def AlbumId(input_url):
    try:
        headers = setProxy()
        res = requests.get(input_url, headers=headers)
        if 'internal error' in res.text:
            return None
    except Exception:
        print_exc()
        return None
    soup = BeautifulSoup(res.text, "html.parser")
    try:
        getAlbumID = soup.select(".play")[0]["onclick"]
        getAlbumID = ast.literal_eval(
            re.search("\[(.*?)\]", getAlbumID).group())[1]
        if getAlbumID is not None:
            return(getAlbumID)
    except Exception:
        print_exc()
        pass


def setProxy():
    base_url = 'https://h.saavncdn.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
    }
    return headers


def getPlayList(listId):
    try:
        response = requests.get(
            'https://www.jiosaavn.com/api.php?listid={0}&_format=json&__call=playlist.getDetails'.format(listId), verify=False)
        if response.status_code == 200:
            response_text = (response.text.splitlines())
            songs_json = list(
                filter(lambda x: x.endswith("}"), response_text))[0]
            songs_json = json.loads(songs_json)
            return songs_json
        return None
    except Exception:
        print_exc()


def getListId(input_url):
    headers = setProxy()
    res = requests.get(input_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    try:
        getPlayListID = soup.select(".flip-layout")[0]["data-listid"]
        if getPlayListID is not None:
            return(getPlayListID)
    except Exception as e:
        print('Unable to scrape Playlist ID', e)
        return None


def getSongsJSON(listId):
    url = 'https://www.jiosaavn.com/api.php?listid=' + \
        str(listId)+'&_format=json&__call=playlist.getDetails'
    response_json = requests.get(url).text
    struct = {}
    try:  # try parsing to dict
        dataform = str(response_json).split('-->')[-1]
        struct = json.loads(dataform)
    except Exception:
        print_exc()
        return None
    return struct


def decrypt_url(url):
    enc_url = base64.b64decode(url.strip())
    dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
    dec_url = dec_url.replace("_96.mp4", "_320.mp3")
    dec_url = dec_url.replace("http://aac.saavncdn.com","https://h.saavncdn.com")
    try:
        r = requests.head(dec_url)
        if r.status_code == 200 or r.status_code == 302:
            return dec_url
        else:
            dec_url = dec_url.replace('_320.mp3', '_160.mp3')
            r = requests.head(dec_url)
            if r.status_code == 200 or r.status_code == 302:
                return dec_url
            else:
                dec_url = dec_url.replace("_160.mp3", "_96.mp3")
                if r.status_code == 200 or r.status_code == 302:
                    return dec_url
    except Exception as e:
        return None
    return None


def fix_title(title):
    title = title.replace('&quot;', '')
    return title


def fix_image_url(url):
    url = str(url)
    url = url.replace('150x150', '500x500')
    return url


def get_lyrics(link):
    try:
        if '/song/' in link:
            link = link.replace("/song/", '/lyrics/')
            source = requests.get(link).text
            soup = BeautifulSoup(source, 'lxml')
            res = soup.find('p', class_='lyrics')
            lyrics = str(res).replace("<br/>", "\n")
            lyrics = lyrics.replace('<p class="lyrics"> ', '')
            lyrics = lyrics.replace("</p>", '')
            return (lyrics)
    except Exception:
        print_exc()
        return
