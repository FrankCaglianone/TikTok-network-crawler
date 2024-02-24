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
def populate_data_structures(followers_list):
    for user in followers_list:
        username = user["username"]

        if username in parsing_list:
            continue
        else:
            parsing_list[username] = 0
            queue.append(username)







# DOCSTRING
def get_all_followers(parsing_user):
    all_followers = []
    url = "https://open.tiktokapis.com/v2/research/user/followers/"
    auth = "Bearer " + access_token
    headers = {
        "Authorization": auth,
        "Content-Type": "application/json"
    }
    cursor = None
    has_more = True

    # Loop to fetch all followers using pagination
    while has_more and len(all_followers) <= 30:
        data = {
            "username": parsing_user,
            "max_count": 10,
        }
        # Add cursor to request if it exists
        if cursor:
            data["cursor"] = cursor

        # Make the post request
        print("sending request")
        response = requests.post(url=url, headers=headers, json=data)

        # Check if request was successful
        if response.status_code == 200:
            json_response = response.json()
            response_data = json_response.get('data')
            all_followers.extend(response_data.get('user_followers'))

            # Check if there are more followers to fetch
            has_more = response_data.get('has_more', False)
            cursor = response_data.get('cursor', None)
        else:
            print("Failed to retrieve followers. Status code:", response.status_code)
            break

    return all_followers






def recursion():
    while queue and len(queue) <= 100:   # Loop until queue is empty
        # Get the first item from the queue
        i = queue.pop(0)

        # Get the user list
        followers_list = get_all_followers(i)

        # Turn the user bit to 1 (parsed)
        parsing_list[i] = 1

        # Populate the dictionary with the newly fetched followers
        populate_data_structures(followers_list)



   
# Declaring Global Variables
starting_user = None
access_token = None
parsing_list = {}  # Maps username to parsed bit (0 or 1)
queue = [] # Queue of username to parse





def main():
    # Get the key and the first user to parse from stdin
    global access_token
    access_token = input("Enter your access token: ")
    global starting_user
    starting_user = input("Please enter the TikTok Username: ")

    
   
    # Add the starting username to list
    parsing_list[starting_user] = 0
    queue.append(starting_user)

    recursion()

    print_dictionary()









main()
   
