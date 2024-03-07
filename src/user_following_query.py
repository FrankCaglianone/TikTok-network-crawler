import requests
import csv
import sys

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
def read_from_file(file_path):
    starting_users = []

    # Open the file and read the contents
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        
        # Loop through the rows in the file
        for row in csv_reader:
            starting_users.append(row[0])
            # print(row[0])    
    return starting_users





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

        # Check request status code
        if response.status_code == 200:
            # If status code is succesfull, proceed
            data = response.json().get('data')
            all_followers.extend(data.get('user_followers'))

            # Check if there are more followers to fetch
            has_more = data.get('has_more', False)
            cursor = data.get('cursor', None)
        elif response.status_code == 401:
            # If status code 401, means the access token it's incorrect, terminate program and try again
            print("Status code 401 Unauthorized: The request has not been applied because it lacks valid authentication credentials for the target resource.")
            sys.exit("Terminating the program due to an error. Please check your access token")
        elif response.status_code == 403:
            # If status code 403, that user cannot be accessed, break, if there are more users in the queue it proceeds, if it is the only user it terminates
            print("Status code 403 Forbidden: The server understood the request but refuses to authorize it.")
            print(f"User not parsed: {parsing_user}")
            break
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





def parse_with_stdin(token):
    # Get the key and the first user to parse from stdin
    global access_token
    access_token = token
    global starting_user
    starting_user = input("Please enter the TikTok Username: ")
    
    # Add the starting username to dictionary and queue
    parsing_list[starting_user] = 0
    queue.append(starting_user)

    # Start parsing
    parse_network()


    print_dictionary()




def parse_with_list(token):
    # Get the key and the path to the list of users to parse
    global access_token
    access_token = token
    file_path = input("Enter the path to your .csv file: ")

    # Get all the starting users to parse from the file
    starting_users = read_from_file(file_path)

    # Add all starting users to the data structures
    for user in starting_users:
        parsing_list[user] = 0
        queue.append(user)

    # Start parsing
    parse_network()

    print_dictionary()


