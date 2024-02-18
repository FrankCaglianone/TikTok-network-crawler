import requests


'''
    This class is used to interact with the TikTok Research API to Query User Followers.
    It makes a post request to the server and returns data in JSON format.
    From that it gets from the JSON response the list of all the followers of the given username.


    Stdin: 
        - access_token: The access token to acces the TikTok Research API is required
        - starting_username: The username of the account you want to query from
    
    Stdout: 
'''


'''
    Response structure example

    "data": {
        "cursor": 1706837834,
        "has_more": true,
        "user_followers": [
            {
                "display_name": "test user",
                "username": "test_username"
            },
            {
                "username": "test user 2",
                "display_name": "test_username2"
            }
        ]
    },
'''




def main(): 
    # API url
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


    # Get the response
    if response.status_code == 200:
        data = response.json().get('data')
        followers_list = data.get('user_followers')

        print("\n")
        print(followers_list)
    else:
        print("Failed to retrieve followers. Status code:", response.status_code)
