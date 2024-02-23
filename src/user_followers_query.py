import requests

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






# Helper functions
def print_dictionary():
    print("Username to Parsed Status:")
    for username, parsed in parsing_list.items():
        print(f"{username}: {parsed}")




# DOCSTRING
def get_response(): 
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
    global starting_username
    starting_username = input("Please enter the TikTok Username: ")
                        

    # Creating the body 
    data = {
        "username": starting_username,  
        "max_count": 10,  # Optional: Adjust the number of results as needed
    }


    # Make the post request
    response = requests.post(url=url, headers=header, json=data)


    # Get the response
    if response.status_code == 200:
        data = response.json().get('data')
        return data
    else:
        print("Failed to retrieve followers. Status code:", response.status_code)


    
# DOCSTRING
def populate_parsing_list(followers_list):
    for user in followers_list:
        username = user["username"]

        if username in parsing_list:
            continue
        else:
            parsing_list[username] = 0






   
# Declaring Global Variables
starting_username = None
parsing_list = {}  # Maps username to parsed bit (0 or 1)




def main():
    res = get_response()
    followers_list = res.get('user_followers')

    # Add the starting username
    parsing_list[starting_username] = 1

    populate_parsing_list(followers_list)
    print_dictionary()







main()
   
