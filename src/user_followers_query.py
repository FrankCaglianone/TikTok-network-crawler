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




# Fetch for a max of 30 users in the get_all_followers() loop
# Fill the queue of users to parse up to only 100 users in parse_network()



# Helper functions
def print_dictionary():
    print("Username to Parsed Status:")
    for username, parsed in parsing_list.items():
        print(f"{username}: {parsed}")




# DOCSTRING
def populate_data_structures(followers_list):

    # Loop through every user in the follower list
    for user in followers_list:
        # Get the username @
        username = user["username"]

        # If already in dictionary skip
        if username in parsing_list:
            continue
        else:
            # Add the new user to the dictionary and the queue
            parsing_list[username] = 0
            queue.append(username)




# DOCSTRING
def get_all_followers(parsing_user):
    all_followers = []
    url = "https://open.tiktokapis.com/v2/research/user/followers/"

    # Create the header
    auth = "Bearer " + access_token
    header = {
        "Authorization": auth,
        "Content-Type": "application/json"
    }

    # Intialize cursor and has_more variables to enter the loop for the first time
    cursor = None
    has_more = True

    # Loop to fetch all followers
    while has_more and len(all_followers) <= 30:
        # Create body
        body = {
            "username": parsing_user,
            "max_count": 10,
        }

        # Add cursor to request if it exists
        if cursor:
            body["cursor"] = cursor

        # Make the post request
        response = requests.post(url=url, headers=header, json=body)

        # Check if request was successful
        if response.status_code == 200:
            data = response.json().get('data')
            all_followers.extend(data.get('user_followers'))

            # Check if there are more followers to fetch
            has_more = data.get('has_more', False)
            cursor = data.get('cursor', None)
        else:
            print("Failed to retrieve followers. Status code:", response.status_code)
            break

    return all_followers





# DOCSTRING
def parse_network():
    # Loop until queue is empty
    while queue and len(queue) <= 100:

        # Get the first item from the queue
        i = queue.pop(0)

        # Get the followers list of that user
        followers_list = get_all_followers(i)

        # Turn the user bit to 1 (parsed)
        parsing_list[i] = 1

        # Populate the dictionary and the queue with the newly fetched followers
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
    
    # Add the starting username to dictionary and queue
    parsing_list[starting_user] = 0
    queue.append(starting_user)

    # Start parsing
    parse_network()


    print_dictionary()








main()
   
