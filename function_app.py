import azure.functions as func
import logging
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def get_token(client_id, client_secret):
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': f'{client_id}',
        'client_secret': f'{client_secret}'
    }

    response = requests.post(url=token_url, headers=headers, data=data)
    return response.json().get('access_token', None)


def get_recommendation():
    client_id = 'b07d29bb3a8b4a7baa5f655acecd94bd'
    client_secret = '926be4feff424d57ba32675ca9d36ceb'
    access_token = get_token(client_id, client_secret)

    track_seed = ''
    artist_seed = '6XyY86QOPPrYVGvF9ch6wz'
    genre_seed = ''

    url = 'https://api.spotify.com/v1/recommendations'

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    params = {
        'limit': 5,
        'seed_artists': artist_seed
    }

    response = requests.get(url=url, params=params, headers=headers)

    recommendation_list = []

    if response.status_code == 200:
        data = response.json()
        print("List of recommendations: ")
        # Extract and print the song names and their artists
        for track in data['tracks']:
            track_name = track['name']
            artists = [artist['name'] for artist in track['artists']]
            recommendation_list.append(f"{track_name} - {' '.join(artists)}")
            # print(f"{track_name} - {' '.join(artists)}")
    else:
        return []

    return recommendation_list


@app.function_name(name="HttpTrigger1")
@app.route(route="recommendation")
def http_trigger1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    song = req.params.get('song')
    if not song:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            song = req_body.get('song')

    if song:
        songs = get_recommendation()
        return func.HttpResponse(f"Hello, {song}===={songs}.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a song in the query string or in the request "
            "body for a personalized response.",
            status_code=200
        )


# @app.function_name(name="HttpTrigger2", methods=[func.HttpMethod.GET])
# @app.route(route="hello")
# def http_trigger2(req: func.HttpRequest) -> func.HttpResponse:
#      return func.HttpResponse("Hello!!!")
    