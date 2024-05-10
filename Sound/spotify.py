################# SPOTIFY API #####################
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json


'''
    @Bilge_AKYOL
    implementation of Spotify API
    the API is used in IdeaBoards and are commented in detail.
'''


load_dotenv()
client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")

def get_token(client_id, client_secret):
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # Spotify API auth tutorial
    # https://developer.spotify.com/documentation/web-api/tutorials/code-flow
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data= {"grant_type":"client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_recc(genre_name):
    token = get_token(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)
    params = {
        'seed_genres': genre_name,
        'market': 'US',
        'limit': 5
    }
    result = get(url, headers=headers, params=params)
    
    if result.status_code == 200:
        json_result = result.json()
        song_names = [track['name'] for track in json_result['tracks']]
        return song_names
    else:
        print("Error:", result.status_code, result.text)
        return None

###################################################