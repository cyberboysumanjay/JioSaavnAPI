import base64
import jiosaavn
from pyDes import *

def format_song(data,lyrics):
    try:
        url = data['media_preview_url']
        url = url.replace("preview", "aac")
        if data['320kbps']=="true":
            url = url.replace("_96_p.mp4", "_320.mp4")
        else:
            url = url.replace("_96_p.mp4", "_160.mp4")
        data['media_url'] = url
    except KeyError or TypeError:
        data['media_url'] = decrypt_url(data['encrypted_media_url'])
        if data['320kbps']!="true":
            data['media_url'] = data['media_url'].replace("_320.mp4","_160.mp4")

    data['song'] = format(data['song'])
    data['music'] = format(data['music'])
    data['singers'] = format(data['singers'])
    data['starring'] = format(data['starring'])
    data['album'] = format(data['album'])
    data["primary_artists"] = format(data["primary_artists"])
    data['image'] = data['image'].replace("150x150","500x500")

    if lyrics:
        if data['has_lyrics']=='true':
            data['lyrics'] = jiosaavn.get_lyrics(data['id'])
        else:
            data['lyrics'] = None

    try:
        data['copyright_text'] = data['copyright_text'].replace("&copy;","©")
    except KeyError:
        pass
    return data

def format_album(data,lyrics):
    data['image'] = data['image'].replace("150x150","500x500")
    data['name'] = format(data['name'])
    data['primary_artists'] = format(data['primary_artists'])
    data['title'] = format(data['title'])
    for song in data['songs']:
        song = format_song(song,lyrics)
    return data

def format_playlist(data,lyrics):
    data['firstname'] = format(data['firstname'])
    data['listname'] = format(data['listname'])
    for song in data['songs']:
        song = format_song(song,lyrics)
    return data

def format(string):
    return string.encode().decode().replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'")

def decrypt_url(url):
    des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0",pad=None, padmode=PAD_PKCS5)
    enc_url = base64.b64decode(url.strip())
    dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
    dec_url = dec_url.replace("_96.mp4", "_320.mp4")
    return dec_url