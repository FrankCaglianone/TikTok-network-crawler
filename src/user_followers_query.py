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

# Create user tests 5 json of up to 5 users



# Helper functions
def print_dictionary():
    print("Username to Parsed Status:")
    for username, parsed in parsing_list.items():
        print(f"{username}: {parsed}")



# DOCSTRING
def get_values():
    print("\n")

    # Get the Access Token from stdin
    global access_token
    access_token = input("Enter your access token: ")

    # Get the starting username from stdin
    global starting_user
    starting_user = input("Please enter the TikTok Username: ")



# DOCSTRING
def get_response(parsing_user): 
    # API url
    url = "https://open.tiktokapis.com/v2/research/user/followers/"

    auth = "Bearer " + access_token


    # Create the Header
    header = {
        "Authorization": auth,
        "Content-Type": "application/json"
    }
                        

    # Creating the body 
    data = {
        "username": parsing_user,  
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



def recursion():
    for i in parsing_list:
        res = get_response(i)
        followers_list = res.get('user_followers')

        parsing_list[i] = 1

        populate_parsing_list(followers_list)



   
# Declaring Global Variables
starting_user = None
access_token = None
parsing_list = {}  # Maps username to parsed bit (0 or 1)




def main():

    # Get the key and the first user to parse
    get_values()


    # Get the first user list
    res = get_response(starting_user)
    followers_list = res.get('user_followers')


    # Add the starting username to list
    parsing_list[starting_user] = 1

    # Populate the dictionary for the first time
    populate_parsing_list(followers_list)


    recursion()




    print_dictionary()







main()
   
