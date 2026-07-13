# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Unofficial JioSaavn API — a small Flask app that proxies/scrapes JioSaavn's internal (undocumented) endpoints and returns clean JSON. There is no test suite, linter, or build step; this is a 5-file app.

## Running locally

```sh
pip3 install -r requirements.txt
python3 app.py
```

Runs at `0.0.0.0:5100` (see bottom of `app.py`) with Flask debug mode and the reloader on.

Production runs via gunicorn (see `Procfile`): `gunicorn app:app --timeout 100 --log-file=-`.

## Deployment

- **Heroku**: via `Procfile` / `app.json`.
- **Vercel**: via `vercel.json`, using `@vercel/python`, routing all paths to `app.py`.
- Runtime pinned to `python-3.8.5` in `runtime.txt`.

There's no CI. Changes are validated by manually hitting endpoints locally.

## Architecture

Request flow: `app.py` (Flask routes) → `jiosaavn.py` (calls JioSaavn's private API, parses responses) → `helper.py` (formats/cleans/decrypts individual song records) → JSON response. `endpoints.py` holds the raw JioSaavn API URL templates used by `jiosaavn.py`.

- **`app.py`**: Flask routes only. Each route pulls `query`/`lyrics`/`songdata`/`id` from query params, does minimal validation, and delegates to `jiosaavn.py`. Routes: `/song/`, `/song/get/`, `/playlist/`, `/album/`, `/lyrics/`, and the universal `/result/` (accepts a raw search query, or a JioSaavn song/album/playlist/featured URL and dispatches based on substring matching).
- **`endpoints.py`**: Base URL strings for JioSaavn's undocumented `api.php` endpoints (search/autocomplete, song details, album details, playlist details, lyrics). If JioSaavn changes its private API, this is usually where fixes start.
- **`jiosaavn.py`**: Talks to JioSaavn. Responses come back JSON-escaped inside text (`.encode().decode('unicode-escape')`) and need a regex fixup (`response.jiosaavn.py`'s `search_for_song`) for stray `(From "Album")`-style quoting before `json.loads`. ID-extraction functions (`get_song_id`, `get_album_id`, `get_playlist_id`) scrape IDs out of raw HTML/JS returned when given a JioSaavn URL, with a fallback split pattern (`try`/`except IndexError`) since JioSaavn's markup varies by content type/page.
- **`helper.py`**: Post-processes raw JioSaavn song/album/playlist dicts — decrypts the media URL (DES/ECB via `pyDes`, key `38346591`), picks 320kbps vs 160kbps stream based on the `320kbps` flag, derives a preview URL, upgrades image URLs to `500x500`, and unescapes HTML entities in text fields (`&quot;`, `&amp;`, `&#039;`).

## Key gotchas for future changes

- JioSaavn's endpoints are undocumented and unstable — expect to need to tweak URL patterns in `endpoints.py` or scraping logic in `jiosaavn.py` when things break upstream.
- The DES decryption key/logic in `helper.py:decrypt_url` is load-bearing for every song's playable URL; don't touch it without a real song response to test against.
- Deploying from outside India can cause degraded/incomplete results (per README) since JioSaavn's API behaves differently by request origin.
