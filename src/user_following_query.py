import requests
import csv
import sys
import atexit
import signal
import datetime

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









# --- Helper functions ---
def print_dictionary():
    print("Username to Parsed Status:")
    for username, parsed in parsing_list.items():
        print(f"{username}: {parsed}")





# --- DATA SAVING FUNCTIONS ---
"""
    Saves data from the `parsing_list` dictionary and the `queue` list into two separate CSV files.

    - The `parsing_list.csv` file will contain two columns: "Username" and "Parsed Status", 
      representing keys and values from the `parsing_list` dictionary, respectively. 
    - The `queue.csv` file will contain a single column: "Usernames to parse", 
      listing all usernames to still parse from the `queue` list.

    Both files are saved with no extra line spaces between rows.
"""
def save_to_csv():
    # Save parsing_list to CSV
    with open('src/outputs/parsing_list.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Parsed Status"])  # Writing headers
        for username, parsed_status in parsing_list.items():
            writer.writerow([username, parsed_status])

    # Save queue to CSV
    with open('src/outputs/queue.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Usernames to parse"]) 
        for username in queue:
            writer.writerow([username])



"""
    Saves a list of time stamps into a CSV file named `time_stamps.csv`.

    The resulting CSV file will contain a single column titled "Time Stamps", 
    with each row containing a time stamp from the `time_stamps` list representing the time 
    at which the response for that username was received since the program started.

    The file is saved with no extra line spaces between rows.
"""
# TODO: fix documentation
def save_time_stamps():
    with open('src/outputs/time_stamps.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Time Stamp"])  # Writing headers
        for username, timestamps in time_stamps.items():
            # If timestamps is None or not a list, log an error or handle it as you see fit
            if timestamps is None:
                print(f"Error: No timestamps found for username {username}.")
                continue  # Skip this username
            elif not isinstance(timestamps, list):
                print(f"Error: Timestamps for username {username} is not a list.")
                continue  # Skip this username

            # Writing username and all its timestamps in one row
            row = [username] + timestamps
            writer.writerow(row)





# TODO: fix the function
def save_jsons():
    with open('src/outputs/saved_jsons.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Json_response"])  # Writing headers
        for username, data in jsons.items():
            writer.writerow([username, data])









# --- HANDLERS FOR DATA SAVING OPERATIONS ---
"""
    Handles the saving of all relevant data structures to CSV files before exiting the application.

    This function sequentially calls:
    - `save_to_csv()` to save parsing-related data and queued usernames to 'parsing_list.csv' and 'queue.csv' respectively.
    - `save_jsons()` to save JSON responses associated with usernames to 'saved_jsons.csv'.
    - `save_time_stamps()` to save time stamps to 'time_stamps.csv'.

    The function ensures that all in-memory data is persisted to disk in a structured CSV format, facilitating later analysis or application restarts.
"""
def cleanup_and_save():
    print("Saving all data to CSV before exiting...")
    save_to_csv()
    save_jsons()
    save_time_stamps()
    

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







# --- CSV DATA RETRIEVAL FUNCTION ---
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










# --- QUEUE MANAGEMENT FUNCTION ---
# TODO: Fixed the bug checking for duplicates in the parse, but need a better time complexity solution
def populate_queue(followers_list):

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









# TODO: DOCSTRING
def get_all_followers(parsing_user):
    # Helper
    json_index = 1
    json_list = []
    tmp = []

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


        elapsed_time = datetime.datetime.now() - start_time
        tmp.append(f"{elapsed_time}")




        # Check request status code
        if response.status_code == 200:
            # If status code is succesfull, proceed
            data = response.json().get('data')
            all_followers.extend(data.get('user_following', []))


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

    jsons[parsing_user] = json_list
    time_stamps[parsing_user] = tmp

    return all_followers, response.status_code





# TODO: DOCSTRING
def parse_network():
    # Loop until queue is empty
    while queue:   # and len(queue) <= 400

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
access_token = None
start_time = None
parsing_list = {}  # Maps username to parsed bit (0 or 1)
queue = [] # Queue of username to parse
jsons = {} # Maps for json files
time_stamps = {} # Map for time stamps





# TODO: DOCSTRING
def parse_with_stdin(token, user_input):
    # Set saving options
    atexit.register(cleanup_and_save)
    signal.signal(signal.SIGINT, handle_signal_received)
    signal.signal(signal.SIGTERM, handle_signal_received)

    # Execute code normally
    try:
        # Get the key and the first user to parse from stdin
        global access_token, start_time
        start_time = datetime.datetime.now()
        access_token = token
        starting_user = user_input
        
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






# TODO: DOCSTRING
def parse_with_list(token, user_input):
     # Set saving options
    atexit.register(cleanup_and_save)
    signal.signal(signal.SIGINT, handle_signal_received)
    signal.signal(signal.SIGTERM, handle_signal_received)

    # Execute code normally
    try: 
        # Get the key and the path to the list of users to parse
        global access_token, start_time
        start_time = datetime.datetime.now()
        access_token = token
        file_path = user_input

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



