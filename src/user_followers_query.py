import requests


url = "https://open.tiktokapis.com/v2/research/user/followers/"


# Get the Access Token from stdin
print("\n")
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



# Response structure
# "data": {
#     "cursor": 1706837834,
#     "has_more": true,
#     "user_followers": [
#         {
#             "display_name": "test user",
#             "username": "test_username"
#         },
#         {
#             "username": "test user 2",
#             "display_name": "test_username2"
#         }
#     ]
# },

# 
if response.status_code == 200:
    data = response.json().get('data')
    followers_list = data.get('user_followers')

    print("\n\n")
    print(followers_list)
else:
    print("Failed to retrieve followers. Status code:", response.status_code)
