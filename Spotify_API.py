import requests

def get_token(client_id, client_secret):
    token_url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(url=token_url, headers=headers, data=data)
    token = response.json().get("access_token", None)
    return f"Bearer {token}"

def get_recommendation(client_id, client_secret, song_id):
    access_token = get_token(client_id, client_secret)

    artist_seed = song_id
    url = "https://api.spotify.com/v1/recommendations"

    headers = {
        "Authorization": access_token,
    }

    params = {"limit": 5, "seed_artists": artist_seed}

    response = requests.get(url=url, params=params, headers=headers)

    recommendation_list = []

    if response.status_code == 200:
        data = response.json()
        for track in data["tracks"]:
            track_name = track["name"]
            artists = [artist["name"] for artist in track["artists"]]
            recommendation_list.append({"name": track_name, "artists": artists})
    return recommendation_list

def search(client_id, client_secret, query, search_type="track", limit=5):
    access_token = get_token(client_id, client_secret)
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": access_token,
    }

    params = {"q": query, "type": search_type, "limit": limit}

    response = requests.get(url=url, params=params, headers=headers)

    search_results = []

    if response.status_code == 200:
        data = response.json()
        for track in data["tracks"]["items"]:
            track_name = track["name"]
            artists = [artist["name"] for artist in track["artists"]]
            search_results.append({"name": track_name, "artists": artists})
    return search_results
