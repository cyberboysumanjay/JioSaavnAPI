import gevent.monkey
gevent.monkey.patch_all()
import requests
from bs4 import BeautifulSoup
from json import JSONDecoder
from pyDes import *
import base64
from urllib.parse import unquote
from sys import platform
import html
import os
import json
import logger
import json
import sys
import ast
import urllib3.request
from traceback import print_exc
import subprocess
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0" , pad=None, padmode=PAD_PKCS5)
base_url = 'http://h.saavncdn.com'
json_decoder = JSONDecoder()
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
}

def fate_proxy():
    resp=requests.get('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list')
    a=((resp.text).split('\n'))
    p_list=[]
    for i in a:
        try:
            p_list.append(json.loads(i))
        except Exception as e:
            continue
    np_list=[]
    for i in p_list:
        if i['country']=='IN':
            np_list.append(i)
    proxy=[]
    fast_proxy=sorted(np_list,key=lambda k: k['response_time'])
    for p in fast_proxy:
      proxy.append(str(p['host'])+':'+str(p['port']))
    return proxy

def get_songs(query,proxies):
    if not query.startswith('https://www.jiosaavn.com'):
        url = "https://www.jiosaavn.com/search/"+query
        flag="link"
    else:
        url=query
        flag="query"
    songs=[]
    try:
        res = requests.get(url, headers=headers, data=[('bitrate', '320')])
        soup = BeautifulSoup(res.text,"lxml")
        all_song_divs = soup.find_all('div',{"class":"hide song-json"})
        for i in all_song_divs:
            try:
                try:
                    song_info= json.loads(i.text)
                    songs.append(song_info)
                except:
                    esc_text = re.sub(r'.\(\bFrom .*?"\)',"",str(i.text))
                    try:
                        song_info = json_decoder.decode(esc_text)
                        songs.append(song_info)
                    except:
                        try:
                            song_info= json.loads(esc_text)
                            songs.append(song_info)
                        except:
                            print(esc_text)

            except Exception as e:
                print_exc()
                continue
        if len(songs)>0:
            return songs
    except Exception as e:
        for test_proxy in proxies:
            try:
                print("Testing with proxy",test_proxy)
                res = requests.get(url, headers=headers, data=[('bitrate', '320')],proxies={"http": test_proxy, "https": test_proxy},timeout=5)
                soup = BeautifulSoup(res.text,"lxml")
                all_song_divs = soup.find_all('div',{"class":"hide song-json"})
                for i in all_song_divs:
                    try:
                        try:
                            song_info= json.loads(i.text)
                            songs.append(song_info)
                        except:
                            song_info = json_decoder.decode(i.text)
                            songs.append(song_info)
                    except Exception as e:
                        #print_exc()
                        continue
            except Exception as e:
                #print_exc()
                continue
            finally:
                if (len(songs)>0):
                    return songs
    return songs

def getAlbum(albumId,proxies):
    songs_json = []
    try:
        response = requests.get('https://www.saavn.com/api.php?_format=json&__call=content.getAlbumDetails&albumid={0}'.format(albumId),verify=False,timeout=4)
        if response.status_code == 200:
           songs_json = list(filter(lambda x: x.startswith("{"), response.text.splitlines()))[0]
           songs_json = json.loads(songs_json)
           return songs_json
    except Exception as e:
       pass
    for p in proxies:
        try:
           response = requests.get(
               'https://www.saavn.com/api.php?_format=json&__call=content.getAlbumDetails&albumid={0}'.format(albumId),
               verify=False,proxies={"http": p, "https": p},timeout=4)
           if response.status_code == 200:
               songs_json = list(filter(lambda x: x.startswith("{"), response.text.splitlines()))[0]
               songs_json = json.loads(songs_json)
               return songs_json
        except Exception as e:
           print("Skipped proxy in album")

    return songs_json

def AlbumId(input_url,proxies):
    try:
        proxi, headers = setProxy()
        res = requests.get(input_url, headers=headers)
        if 'internal error' in res.text:
            for p in proxies:
                try:
                    res = requests.get(input_url,proxies={"http": p, "https": p}, headers=headers,timeout=4)
                    if 'internal error' in res.text:
                        continue
                    break
                except Exception as e:
                    print("Skipped this proxy")
    except Exception as e:
        logger.error('Error accessing website error: ' + e)

    soup = BeautifulSoup(res.text, "html.parser")
    try:
        getAlbumID = soup.select(".play")[0]["onclick"]
        getAlbumID = ast.literal_eval(re.search("\[(.*?)\]", getAlbumID).group())[1]
        if getAlbumID is not None:
            return(getAlbumID)
    except Exception as e:
        print(e)
        pass

def setProxy():
    base_url = 'http://h.saavncdn.com'
    proxy_ip = ''
    if ('http_proxy' in os.environ):
        proxy_ip = os.environ['http_proxy']
    proxies = {
        'http': proxy_ip,
        'https': proxy_ip,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
    }
    return proxies, headers

def getPlayList(listId,proxies):
    songs_json = []
    try:
        response = requests.get('https://www.jiosaavn.com/api.php?listid={0}&_format=json&__call=playlist.getDetails'.format(listId), verify=False)
        if response.status_code == 200:
            response_text=(response.text.splitlines())
            songs_json = list(filter(lambda x: x.endswith("}"), response_text))[0]
            songs_json = json.loads(songs_json)
        return songs_json
    except Exception as e:
        print(e)
        proxies=fate_proxy()
        for proxy in proxies:
            try:
                response = requests.get('https://www.jiosaavn.com/api.php?listid={0}&_format=json&__call=playlist.getDetails'.format(listId), verify=False,proxies={'http':proxy,'https': proxy})
                if response.status_code == 200:
                    songs_json = list(filter(lambda x: x.endswith("}"), response.text.splitlines()))[0]
                    songs_json = json.loads(songs_json)
                return songs_json
            except Exception:
                pass
    return songs_json

def getListId(input_url,proxies):
    p, headers = setProxy()
    try:
        res = requests.get(input_url, headers=headers)
        if 'internal error' in res.text:
            proxies=fate_proxy()
            for proxy in proxies:
                try:
                    res = requests.get(input_url, proxies={"http": proxy, "https": proxy}, headers=headers)
                    if 'internal error' in res.text:
                        continue
                    break
                except Exception as e:
                    print("Skipped this proxy")
        #res = requests.get(input_url, proxies={"http": proxy, "https": proxy}, headers=headers)
        #res = requests.get(input_url)
    except Exception as e:
        print_exc()

    soup = BeautifulSoup(res.text, "html.parser")
    #print(soup)

    try:
        getPlayListID = soup.select(".flip-layout")[0]["data-listid"]
        if getPlayListID is not None:
            return(getPlayListID)
    except Exception as e:
        print('Unable to scrape Playlist ID',e)

def getSongsJSON(listId,proxies):
    url='https://www.jiosaavn.com/api.php?listid='+str(listId)+'&_format=json&__call=playlist.getDetails'
    response_json=requests.get(url).text
    struct = {}
    try: #try parsing to dict
        dataform = str(response_json).split('-->')[-1]
        #print(dataform)
        struct = json.loads(dataform)
    except Exception as e:
        print(e)
        print("Error Occured while parsing json")
    return struct

def decrypt_url(url):
    enc_url = base64.b64decode(url.strip())
    dec_url = des_cipher.decrypt(enc_url,padmode=PAD_PKCS5).decode('utf-8')
    dec_url = base_url + dec_url[10:] + '_320.mp3'
    return dec_url

def fix_title(title):
    title=title.replace('&quot;','')
    return title

def fix_image_url(url):
    url=str(url)
    url=url.replace('150x150','500x500')
    return url
