import requests


url = "https://open.tiktokapis.com/v2/research/user/followers/"


# Get the Access Token from stdin
access_token = input("Enter your access token: ")
auth = "Bearer " + access_token


# Create the Header
header = {
    "Authorization": auth,
    "Content-Type": "application/json"
}


# Get the starting username from stdin
starting_username = input("Please enter the TikTok Username: ")
                          

# Creating the body 
dat = {
    "username": starting_username,  
    "max_count": 10,  # Optional: Adjust the number of results as needed
}


# Make the post request
response = requests.post(url=url, headers=header, json=dat)



if response.status_code == 200:
    followers = response.json()
    print(followers)
else:
    print("Failed to retrieve followers. Status code:", response.status_code)
