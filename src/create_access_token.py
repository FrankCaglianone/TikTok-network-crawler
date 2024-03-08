import requests
import sys



def get_token(key, secret):
    # Authentication endpoint from TikTok's documentation
    auth_url = 'https://open.tiktokapis.com/v2/oauth/token/'

    # Creating the header
    head = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache"
    }


    # Creating body
    body = {
        "client_key" : key,
        "client_secret" : secret,
        "grant_type" : "client_credentials"
    }


    # Making the authentication request
    auth_response = requests.post(auth_url, headers = head, data = body)


    # Get the response
    if auth_response.status_code == 200:
        if auth_response.json().get('access_token') is None:
            sys.exit('Authentication failed, please check your credentials')
        else:
            token = auth_response.json().get('access_token')
            expiration = auth_response.json().get('expires_in')
            type = auth_response.json().get('token_type')

            print("\n")
            print("Access Token: ", token)
            print("Expiration in seconds: ", expiration)
            print("Token Type: ", type)

            return token
    else:
        sys.exit("Failed to obtain access token. Status code:", auth_response.status_code)
