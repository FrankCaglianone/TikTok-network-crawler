import requests

# Authentication endpoint from TikTok's documentation
auth_url = 'https://open.tiktokapis.com/v2/oauth/token/'


# Get key and secret from the standard input
print("\n")
client_key = input("Please insert your key: ")
client_secret = input("Please insert your secret: ")


# Creating the header
head = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Cache-Control": "no-cache"
}


# Creating body
body = {
    "client_key" : client_key,
    "client_secret" : client_secret,
    "grant_type" : "client_credentials"
}


# Making the authentication request
auth_response = requests.post(auth_url, headers = head, data = body)


# Get the response
if auth_response.status_code == 200:
    if auth_response.json().get('access_token') is None:
        print('Authentication failed, please check your credentials')
    else:
        token = auth_response.json().get('access_token')
        expiration = auth_response.json().get('expires_in')
        type = auth_response.json().get('token_type')

        print("\n")
        print("Access Token: ", token)
        print("Expiration in seconds: ", expiration)
        print("Token Type: ", type)
else:
    print("Failed to obtain access token. Status code:", auth_response.status_code)
