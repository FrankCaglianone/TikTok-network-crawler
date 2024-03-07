import requests
import csv
import sys
import csv
import atexit
import signal

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


def save_to_csv():
    # Save parsing_list to CSV
    with open('parsing_list.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Parsed Status"])  # Writing headers
        for username, parsed_status in parsing_list.items():
            writer.writerow([username, parsed_status])

    # Save queue to CSV
    with open('queue.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Usernames to parse"]) 
        for username in queue:
            writer.writerow([username])


def cleanup_and_save():
    print("Saving data to CSV before exiting...")
    save_to_csv()
    



def handle_signal_received():
    cleanup_and_save()
    exit(0)



def read_from_csv(file_path):
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
def populate_queue(followers_list):

    # Loop through every user in the follower list
    for user in followers_list:
        # Get the username @
        username = user["username"]

        # If already in dictionary skip
        if username in parsing_list:
            continue
        else:
            # Add the new user to the queue
            queue.append(username)




# DOCSTRING
def get_all_followers(parsing_user):
    # To return
    all_followers = []

    # url to send the request
    url = "https://open.tiktokapis.com/v2/research/user/following/"

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
            all_followers.extend(data.get('user_following'))

            # Check if there are more followers to fetch
            has_more = data.get('has_more', False)
            cursor = data.get('cursor', None)
        elif response.status_code == 401:
            # If status code 401, means the access token it's incorrect, terminate program and try again
            print("Status code 401 Unauthorized: The request has not been applied because it lacks valid authentication credentials for the target resource.")
            sys.exit("Terminating the program due to an error. Please check your access token")
        elif response.status_code == 403:
            # If status code 403, that user cannot be accessed, break, if there are more users in the queue it proceeds, if it is the only user it terminates
            break
        elif response.status_code == 500:
            # Internal Server Error: This indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
            break
        else:
            print("Failed to retrieve followers. Status code:", response.status_code)
            break

    return all_followers, response.status_code





# DOCSTRING
def parse_network():
    # Loop until queue is empty
    while queue and len(queue) <= 100:

        # Get the first item from the queue
        i = queue.pop(0)

        # Get the followers list of that user and the status code
        followers_list, code = get_all_followers(i)

        # Add user to dictionary with corresponding bit
        if code == 200: 
            # parsed
            parsing_list[i] = 1
        elif code == 403:
            # User cannot be accessed
            parsing_list[i] = 2
        elif code == 500:
            # User not existent or not found
            parsing_list[i] = 3
        else: 
            # Unkown
            parsing_list[i] = 4


        # Populate the dictionary and the queue with the newly fetched followers
        populate_queue(followers_list)




   
# Declaring Global Variables
starting_user = None
access_token = None
parsing_list = {}  # Maps username to parsed bit (0 or 1)
queue = [] # Queue of username to parse





def parse_with_stdin(token):
    # Set saving options
    atexit.register(cleanup_and_save)
    signal.signal(signal.SIGINT, handle_signal_received)
    signal.signal(signal.SIGTERM, handle_signal_received)

    # Execute code normally
    try: 
        # Get the key and the first user to parse from stdin
        global access_token
        access_token = token
        global starting_user
        starting_user = input("Please enter the TikTok Username: ")
        
        # Add the starting username to dictionary and queue
        queue.append(starting_user)

        # Start parsing
        parse_network()


        print_dictionary()
    except Exception as e:
        # If exception is catched save and close
        cleanup_and_save()
        print(f"Unhandled exception: {e}")




def parse_with_list(token):
     # Set saving options
    atexit.register(cleanup_and_save)
    signal.signal(signal.SIGINT, handle_signal_received)
    signal.signal(signal.SIGTERM, handle_signal_received)

    # Execute code normally
    try: 
        # Get the key and the path to the list of users to parse
        global access_token
        access_token = token
        file_path = input("Enter the path to your .csv file: ")

        # Get all the starting users to parse from the file
        starting_users = read_from_csv(file_path)

        # Add all starting users to the data structures
        for user in starting_users:
            queue.append(user)

        # Start parsing
        parse_network()

        print_dictionary()
    except Exception as e:
        # If exception is catched save and close
        cleanup_and_save()
        print(f"Unhandled exception: {e}")




