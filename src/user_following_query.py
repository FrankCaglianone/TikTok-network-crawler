import argparse
import requests
import csv
import sys
import atexit
import signal
import datetime
import create_access_token
import threading
import time


import save_files

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









# ########## Helper functions ##########
def print_dictionary():
    print("Username to Parsed Status:")
    for username, parsed in parsing_list.items():
        print(f"{username}: {parsed}")







########## HANDLERS FOR DATA SAVING OPERATIONS ##########
"""
    Handles the saving of all relevant data structures to CSV files before exiting the application.

    This function sequentially calls:
    - `save_to_csv()` to save parsing-related data and queued usernames to 'parsing_list.csv' and 'queue.csv' respectively.
    - `save_jsons()` to save JSON responses associated with usernames to 'saved_jsons.csv'.
    - `save_time_stamps()` to save time stamps to 'time_stamps.csv'.
    - 'save_network()' to save network connections to 'network.csv'.

    The function ensures that all in-memory data is persisted to disk in a structured CSV format, facilitating later analysis or application restarts.
"""
def cleanup_and_save():
    print("Saving all data to CSV before exiting...")
    save_files.save_to_csv(parsing_list, queue)
    save_files.save_jsons(jsons)
    save_files.save_time_stamps(time_stamps)
    save_files.save_network(network_graph)

    

"""
    Responds to a termination signal by ensuring all data is safely saved before exiting the application.

    When a signal (e.g., SIGINT from a keyboard interrupt, or another termination signal) is received, this function:
    1. Calls `cleanup_and_save()` to perform all necessary data saving operations, ensuring no data loss occurs.
    2. Exits the application with a status code of 0, indicating a clean and intentional shutdown.

    This function is registered as a handler for termination signals to ensure graceful exits.
"""
def handle_signal_received():
    cleanup_and_save()
    exit(0)







########## CSV DATA RETRIEVAL FUNCTION ##########
"""
    This function opens a CSV file located at the given file_path, reads its contents,
    and appends the first item of each row to a list. This list is then returned. The
    function is designed to handle UTF-8 encoded CSV files.

    Parameters:
        file_path (str): The path to the CSV file to be read.

    Returns:
        list: A list of strings, each representing the first column's value from each row in the CSV file.

    Raises:
        SystemExit: If the file at the specified path is not found, or if an unexpected error occurs during file reading, 
                    the function will print an error message and terminate the execution of the program.
"""
def read_from_csv(file_path):
    starting_users = []

    try:
        # Open the file and read the contents
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            
            # Loop through the rows in the file
            for row in csv_reader:
                starting_users.append(row[0])
                # print(row[0])
        #
    except FileNotFoundError:
        # If the file is not found, print an error message and exit the program
        sys.exit(f"Error: The file at {file_path} was not found.") 
    except Exception as e: 
        # If any other exception occurs, exit the program
        sys.exit(f"Error: {e}") 
    return starting_users










########## QUEUE & NETWORK MANAGEMENT FUNCTION ##########
"""
    Adds the followees that still need to be parsed to the global queue for further processing.
    Saves their relationship with the parsing user in a global network graph.

    This function iterates over a list of followers, each represented as a dictionary with "username" key and "display_name" value.
    It adds each unique followee's username to the global queue unless the username already exists in either the global parsing list or the queue itself. 
    Additionally, it records the relationship between the parsing user and each follower by appending a tuple to a global network graph data structure.

    Parameters:
    - followers_list (list of tuples): A list of tuples composed by "username" key and "display_name" value.
    - parsing_user (str): The username of the user whose followees are being added. 
"""
def populate_queue_and_network(followers_list, parsing_user):
    # Loop through every user in the follower list
    for user in followers_list:
        # Get the username @
        username = user["username"]

        # If already in dictionary skip
        if username in parsing_list or username in queue:
            continue
        else:
            # Add the new user to the queue
            queue.append(username)
        
        tmp = (parsing_user, username)
        network_graph.append(tmp)










"""
    Retrieves all followees for a given user from the TikTok API, handling pagination and rate limits.

    This function makes a series of POST requests to the TikTok API to fetch the complete list of followees for the specified user. 
    It handles pagination by using a cursor, and continues to fetch data until all followers are retrieved or until an error occurs. 
    Additionally, it tracks the response time for each request to monitor performance.

    Parameters:
    - parsing_user (str): The username of the TikTok user whose followers are to be retrieved.

    Returns:
    - tuple:
        - all_followers (list): A list of tuples, each representing a follower, composed of "display_name" and "username".
        - status_code (int): The HTTP status code of the last API request. Useful for identifying if the fetch was successful (200) or if it encountered issues (e.g., 401, 403, 500).

    Notes:
    - This function updates two global variables: `jsons` and `time_stamps`. `jsons` stores the JSON response for each user, and `time_stamps` keeps track of the elapsed time for each API call.
    - The function uses a `while` loop with the condition `has_more` to manage pagination, controlled by the API's response indicating more data is available.

    Exceptions:
    - Exits the program if a 401 Unauthorized status code is encountered, indicating invalid authentication credentials.
    - In case of 403 Forbidden or 500 Internal Server Error, the loop is exited, but the program does not terminate, allowing for the possibility of subsequent operations with other users.
"""
def get_all_followers(parsing_user):
    global post_requests

    # Helper
    json_list = []
    tmp = []
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
    while has_more:    # and len(all_followers) <= 100
        # Create body
        body = {
            "username": parsing_user,
            "max_count": 100,
        }

        # Add cursor to request if it exists
        if cursor:
            body["cursor"] = cursor

        # Make the post request
        response = requests.post(url=url, headers=header, json=body)
        post_requests += 1

        # Append the timestamp of that response to the list
        elapsed_time = datetime.datetime.now() - start_time
        tmp.append(f"{elapsed_time}")


        # Check request status code
        if response.status_code == 200:
            # If status code is succesfull, proceed
            data = response.json().get('data')

            # Append list of following to all_followers[] or append an empty list in case there are 0 followings
            all_followers.extend(data.get('user_following', []))

            # Append the json response to the list
            json_list.append(data)

            # Check if there are more followers to fetch
            has_more = data.get('has_more', False)
            cursor = data.get('cursor', None)
        elif response.status_code == 401:
            # If status code 401, means the access token it's incorrect, terminate program and try again
            print("Status code 401 Unauthorized: The request has not been applied because it lacks valid authentication credentials for the target resource.")
            sys.exit("Terminating the program due to an error. Please check your access credentials")
        elif response.status_code == 403:
            # If status code 403, that user cannot be accessed, break, if there are more users in the queue it proceeds, if it is the only user it terminates
            break
        elif response.status_code == 500:
            # Internal Server Error: This indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
            break
        else:
            print("Failed to retrieve followers. Status code:", response.status_code)
            break
    
    # Append the list of jsons and the list of timestamps to the global data structures
    jsons[parsing_user] = json_list
    time_stamps[parsing_user] = tmp

    return all_followers, response.status_code





"""
    Processes users in a global queue by fetching their followees and updating the network graph and parsing status.

    This function repeatedly removes users from a global queue, fetches their followees via the `get_all_followers` function, 
    and then categorizes each user based on the HTTP status code returned from the attempt to fetch their followers. 
    
    It updates a global parsing list with the status of each user processed:
        - 1 if the user's followers were successfully fetched (200),
        - 2 if the user cannot be accessed (403),
        - 3 if the user does not exist or was not found (500),
        - 4 for any other response codes, indicating an unknown issue.

    For each user processed successfully (code 200), their followers are added to the queue for future processing, 
    and the relationship between the user and each follower is added to the global network graph.

    Notes:
    - The function modifies the global `queue`, `parsing_list`, and `network_graph` variables.
    - The loop continues until the `queue` is empty, ensuring that the network is parsed as comprehensively as possible given the initial set of users.
    - This function relies on `get_all_followers` to fetch follower data and `populate_queue_and_network` to add new users to the queue and update the network graph.
"""
def parse_network():
    global post_requests

    # Loop until queue is empty
    while queue:   # and len(queue) <= 400
        if(post_requests < 18000):
            # Get the first item from the queue
            i = queue.pop(0)

            # Get the followees list of that user and the status code
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


            # Populate the dictionary and the queue with the newly fetched followees
            # Enters the loop only if status code = 200, because follower_list is empty.
            populate_queue_and_network(followers_list, i)
        
        else:
            print("Rate limit reached. Going to sleep until reset at 12 AM UTC.")
            current_time = datetime.datetime.utcnow()
            reset_time = datetime.datetime.combine(current_time.date() + datetime.timedelta(days=1), datetime.time(0))
            sleep_seconds = (reset_time - current_time).total_seconds()
            print(f"Current time: {current_time}, Reset time: {reset_time}, Sleep for {sleep_seconds} seconds")
            time.sleep(sleep_seconds)
            post_requests = 0  # Reset the request counter after sleep










########## Token Creation Functions ##########
condition = threading.Condition()  # Condition variable for synchronizing access to access_token


# Use multithreading to instantiate a timer to create an access token every ~ 2 hours
def create_tokens():
    # Access Global Variables
    global access_token, key, secret
    while True:
        # Simulate access token creation
        with condition:
            access_token = create_access_token.get_token(key, secret)
            print(f"New Key Created: {access_token} \n")
            condition.notify_all() # Notify all waiting threads that the token is updated
        time.sleep(6000) # Sleep for 2 hours, 7200s, use 7000




# Wait for the access token to be available.
def wait_for_token():
    global access_token
    with condition:
        while access_token is None:
            condition.wait()  # Wait until the access token is updated









   
########## Declaring Global Variables ##########
access_token = None
key = None
secret = None
start_time = None
post_requests = 0



########## Declaring Global Data Structures ##########
parsing_list = {}  # Maps the username to its parsed bit.
queue = [] # Queue of all username to still be parsed.
jsons = {} # Maps each username to a list of all its json responses.
time_stamps = {} # Maps each username to a list of all the timestamps of its json responses.
network_graph = []









########## NETWORK PARSING FUNCTIONS ##########
"""
    Initiates parsing based on a username provided through the terminal command line.

    This function configures signal handlers and a cleanup routine to ensure graceful shutdown and data saving. 
    It starts the parsing process with a single user input as the initial point.

    Parameters:
    - token (str): Authentication token used for parsing operations.
    - user_input (str): The username of the starting point for parsing.

    After setting up, it adds the starting username to a global queue and begins the network parsing process.
    In case of an exception, it ensures that cleanup and save operations are called before termination.

    Note:
    - This function modifies global variables and relies on external functions like `cleanup_and_save`,
        `handle_signal_received`, and `parse_network` for its operations.
    - It catches and handles any exceptions, ensuring that the cleanup function is always called.
"""
def parse_with_stdin(stdin_key, stdin_secret, user_input):
    # Set saving options
    atexit.register(cleanup_and_save)
    signal.signal(signal.SIGINT, handle_signal_received)
    signal.signal(signal.SIGTERM, handle_signal_received)

    # Execute code normally
    try:
        # Get the key and the first user to parse from stdin
        global key, secret, start_time
        start_time = datetime.datetime.now()
        key = stdin_key
        secret = stdin_secret
        starting_user = user_input


        ##### Start the thread to create the access tokens #####
        # Create a thread that will execute the create_tokens function
        # Daemon threads are stopped automatically when the main program exits
        # Start the thread
        threading.Thread(target=create_tokens, daemon=True).start()

        # Wait for the first access token to be available
        wait_for_token()
        
        
        # Add the starting username to dictionary and queue
        queue.append(starting_user)

        # Start parsing
        parse_network()


        cleanup_and_save()
        print_dictionary()
    except Exception as e:
        # If exception is catched save and close
        cleanup_and_save()
        print(f"Unhandled exception: {e}")





"""
    Initiates parsing based on a list of users obtained from a specified file.

    Similar to `parse_with_stdin`, this function sets up signal handlers and a cleanup routine for graceful shutdown and data saving. 
    Instead of starting with a single user input, it reads a list of users from a provided file path and adds them to the global queue for parsing.

    Parameters:
    - token (str): Authentication token used for parsing operations.
    - user_input (str): The file path containing the list of users to start parsing from.

    The function reads the initial list of users to parse from the specified file and proceeds with the network parsing process. 
    It ensures that cleanup and save operations are executed in case of an exception.

    Note:
    - This function modifies global variables and relies on external functions like `cleanup_and_save`,
      `handle_signal_received`, `read_from_csv`, and `parse_network` for its operations.
    - Exception handling is implemented to ensure cleanup is always performed.
"""
def parse_with_list(stdin_key, stdin_secret, user_input):
     # Set saving options
    atexit.register(cleanup_and_save)
    signal.signal(signal.SIGINT, handle_signal_received)
    signal.signal(signal.SIGTERM, handle_signal_received)

    # Execute code normally
    try: 
        # Get the key and the path to the list of users to parse
        global key, secret, start_time
        start_time = datetime.datetime.now()
        key = stdin_key
        secret = stdin_secret
        file_path = user_input


        ##### Start the thread to create the access tokens #####
        # Create a thread that will execute the create_tokens function
        # Daemon threads are stopped automatically when the main program exits
        # Start the thread
        threading.Thread(target=create_tokens, daemon=True).start()

        # Wait for the first access token to be available
        wait_for_token()


        # Get all the starting users to parse from the file
        starting_users = read_from_csv(file_path)

        # Add all starting users to the data structures
        for user in starting_users:
            queue.append(user)

        # Start parsing
        parse_network()


        cleanup_and_save()
        print_dictionary()
    except Exception as e:
        # If exception is catched save and close
        cleanup_and_save()
        print(f"Unhandled exception: {e}")









if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate user queries with provided credentials.")

    parser.add_argument("key", help="API key for authentication.")
    parser.add_argument("secret", help="API secret for authentication.")
    parser.add_argument("user_input", help="Path to the usernames input or a single username. Ends with .csv for list input.")

    args = parser.parse_args()

    # Set global variables
    key = args.key
    secret = args.secret
    user_input = args.user_input


    # Determine how to handle user input based on the file extension
    if user_input.endswith('.csv'):
        parse_with_list(key, secret, user_input)
    else:
        parse_with_stdin(key, secret, user_input)