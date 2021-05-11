## JioSaavn API [Unofficial]

### Show some :heart: and :star: the repo to support the project

[![GitHub stars](https://img.shields.io/github/stars/cyberboysumanjay/jiosaavnapi.svg?style=social&label=Star)](https://github.com/cyberboysumanjay/JioSaavnAPI) ![GitHub followers](https://img.shields.io/github/followers/cyberboysumanjay.svg?style=social&label=Follow)
[![Telegram Channel](https://img.shields.io/badge/Telegram-Channel-orange)](https://t.me/sjprojects)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

#### JioSaavn API written in Python using Flask  

 ---
###### **NOTE:** You don't need to have JioSaavn link of the song in order to fetch the song details, you can directly search songs by their name. Fetching Songs/Albums/Playlists from URL is also supported in this API.  

 ---

### **Features**:
##### Currently the API can get the following details for a specific song in JSON format:
- **Song Name**
- **Singer Name**
- **Album Name**
- **Album URL**
- **Duration of Song**
- **Song Thumbnail URL (Max Resolution)**
- **Song Language**
- **Download Link**
- **Release Year**
- **Album Art Link (Max Resolution)**
- **Lyrics**
- .... and much more!

```json
{
    "album": "BIBA",
    "album_url": "https://www.jiosaavn.com/album/biba/98G3uzIs2qQ_",
    "autoplay": "false",
    "duration": "175",
    "e_songid": "ICERW0MFfQs",
    "has_rbt": "false",
    "image_url": "https://c.saavncdn.com/987/BIBA-English-2019-20190201201359-500x500.jpg",
    "label": "Joytime Collective",
    "label_url": "/label/joytime-collective-albums/",
    "language": "hindi",
    "liked": "false",
    "map": "Marshmello^~^/artist/marshmello-songs/Eevs5FiVgus_^~^Pritam Chakraborty^~^/artist/pritam-chakraborty-songs/OaFg9HPZgq8_^~^Shirley Setia^~^/artist/shirley-setia-songs/9qGdjoPJ1vM_^~^Pardeep Singh Sran^~^/artist/pardeep-singh-sran-songs/NIfiZRCrYQA_^~^Dev Negi^~^/artist/dev-negi-songs/NpCqdI4dD5U_",
    "music": "",
    "origin": "search",
    "origin_val": "biba",
    "page": 1,
    "pass_album_ctx": "true",
    "perma_url": "https://www.jiosaavn.com/song/biba/ICERW0MFfQs",
    "publish_to_fb": true,
    "singers": "Marshmello, Pritam Chakraborty, Shirley Setia, Pardeep Singh Sran, Dev Negi",
    "songid": "PIzj75J8",
    "starred": "false",
    "starring": "",
    "streaming_source": null,
    "tiny_url": "https://www.jiosaavn.com/song/biba/ICERW0MFfQs",
    "title": "BIBA",
    "twitter_url": "http://twitter.com/share?url=https%3A%2F%2Fwww.jiosaavn.com%2Fsong%2Fbiba%2FICERW0MFfQs&text=%23NowPlaying+%22BIBA%22+%40jiosaavn+%23OurSoundtrack&related=jiosaavn",
    "url": "http://h.saavncdn.com/987/cd902d048c13e5ce6ca84cc409746a5d.mp3",
    "year": "2019"
  }
```

### **Installation**:

Clone this repository using
```sh
$ git clone https://github.com/cyberboysumanjay/JioSaavnAPI
```
Enter the directory and install all the requirements using
```sh
$ pip3 install -r requirements.txt
```
Run the app using
```sh
$ python3 app.py
```
Navigate to 127.0.0.1:5000 to see the Homepage

### **Usage**:
Fetching lyrics is optional and is triggered only when it is passed as an argument in the GET Request. (**&lyrics=true**)
**If you enable lyrics search, it will take more time to fetch results**

---
##### **Universal Endpoint**: (Supports Song Name, Song Link, Album Link, Playlist Link)
```sh
http://127.0.0.1:5000/result/?query=<insert-jiosaavn-link-or-query-here>&lyrics=true
```
**Example:** Navigate to http://127.0.0.1:5000/result/?query=alone to get a JSON response of songs data in return.

----


##### **Song URL Endpoint**:
```sh
http://127.0.0.1:5000/song/?query=<insert-jiosaavn-song-link>&lyrics=true
```
**Example:** Navigate to http://127.0.0.1:5000/song/?query=https://www.jiosaavn.com/song/khairiyat/PwAFSRNpAWw to get a JSON response of song data in return.

---

##### **Playlist URL Endpoint**:
```sh
http://127.0.0.1:5000/playlist/?query=<insert-jiosaavn-playlist-link>&lyrics=true
```
**Example:** Navigate to http://127.0.0.1:5000/playlist/?query=https://www.jiosaavn.com/featured/romantic-hits-2020---hindi/ABiMGqjovSFuOxiEGmm6lQ__ to get a JSON response of playlist data in return.

---

##### **Album URL Endpoint**:
```sh
http://127.0.0.1:5000/album/?query=<insert-jiosaavn-album-link>&lyrics=true
```
**Example:** Navigate to http://127.0.0.1:5000/album/?query=https://www.jiosaavn.com/album/chhichhore/V4F3M5,cNb4_ to get a JSON response of album data in return.

---

##### **Lyrics Endpoint**:
```sh
http://127.0.0.1:5000/lyrics/?query=<insert-jiosaavn-song-link-or-song-id>&lyrics=true
```
**Example:** Navigate to http://127.0.0.1:5000/lyrics/?query=https://www.jiosaavn.com/song/khairiyat/PwAFSRNpAWw to get a JSON response of lyrics data in return.

---

#### You can fork the repo and deploy on VPS or deploy it on Heroku :)  

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/cyberboysumanjay/JioSaavnAPI/tree/master)

**Note:** Heroku gives US/Europe servers which won't be able to fetch all songs flawlessly. Use any Indian VPS for accurate results.

---

## **Made using this API** :heart:
#### [Musify](https://github.com/Harsh-23/Musify/releases) - Android App
#### [@songdl_bot](https://telegram.dog/songdl_bot) - Song Downloader Bot on Telegram
#### [Jio-Saavn-Downloader [Beta]](https://jiosaavn.netlify.app/) - [Open Sourced](https://github.com/ParveenBhadooOfficial/Jio-Saavn-Downloader) website made by [Praveen Bhadoo](https://github.com/ParveenBhadooOfficial)
#### [Musicder](https://musicder.tk/) - [Open Sourced](https://github.com/cachecleanerjeet/Musicder) website made by [Tuhin Pal](https://github.com/cachecleanerjeet)
#### [Music_Downloader_CLI](https://github.com/thehamkercat/Music_Downloader_CLI) made by [TheHamkerCat](https://github.com/thehamkercat)
#### Star the Repo in case you liked it :)

### © [Sumanjay](https://cyberboysumanjay.github.io)
