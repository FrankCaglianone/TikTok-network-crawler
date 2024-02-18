import requests


'''
    This class is used to interact with the TikTok Research API to Query User Followers.
    It makes a post request to the server and returns data in JSON format.
    From that it gets from the JSON response the list of all the liked videos of the given username.


    Stdin: 
        - access_token: The access token to acces the TikTok Research API is required
        - starting_username: The username of the account you want to query from
    
    Stdout: 
'''


'''
    Response structure example

    "data": {
        "cursor": 1706457371000,
        "has_more": true,
        "user_liked_videos": [
            {
                "share_count": 1,
                "view_count": 1586,
                "comment_count": 6,
                "hashtag_names": [
                    "song",
                    "Viral"
                ],
                "id": 123123123123123123123,
                "music_id": 454545454545454545
            },
        ]
    },
'''



 
# API url with Fields
# All field options available: fields = id, create_time, username, region_code, video_description, music_id, like_count, comment_count, share_count, view_count, hashtag_names
fields = "id,create_time,username,region_code"
url = f"https://open.tiktokapis.com/v2/research/user/liked_videos/?fields={fields}"


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


# Get the response
if response.status_code == 200:
    data = response.json().get('data')
    liked_videos_list = data.get('user_liked_videos')

    print("\n")
    print(liked_videos_list)
else:
    print("Failed to retrieve liked videos. Status code:", response.status_code)
    error_details = response.json()
    print("Error details:", error_details)
