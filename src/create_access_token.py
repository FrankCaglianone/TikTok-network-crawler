import requests

# Authentication endpoint from TikTok's documentation
auth_url = 'https://open.tiktokapis.com/v2/oauth/token/'


# Get key and secret from the standard input
print("\n")
print("Please insert your key")
client_key = input()
print("Please insert your secret")
client_secret = input()


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


# Check if the request was successful
if auth_response.status_code == 200:
    token = auth_response.json().get('access_token')
    expiration = auth_response.json().get('expires_in')
    type = auth_response.json().get('token_type')

    print("\n")
    print("Access Token: ", token)
    print("Expiration in seconds: ", expiration)
    print("Token Type: ", type)
else:
    print("Failed to obtain access token. Status code:", auth_response.status_code)
