import argparse
import atexit
import csv
import datetime
import signal
import sys
import threading
import time
import requests
from datetime import date, timedelta

import create_access_token
import save_files





########## HANDLERS FOR DATA SAVING OPERATIONS ##########
def cleanup_and_save():
    print("Saving all data to CSV before exiting...")
    save_files.save_all_data_structures(users_hashtags_dict, users_queue, hashtags_list)



def handle_signal_received():
    cleanup_and_save()
    exit(0)







########## CSV DATA RETRIEVAL FUNCTION ##########
def read_from_csv(file_path):
    users = []

    try:
        # Open the file and read the contents
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header
            # Loop through the rows in the file
            for row in csv_reader:
                if row:  # Check if the row is not empty
                    users.append(row[0])  # Assume the user's name is in the first column
                else:
                    sys.exit("Warning: Found an empty row in the CSV.")
        #
    except FileNotFoundError:
        # If the file is not found, print an error message and exit the program
        sys.exit(f"Error: The file at {file_path} was not found.") 
    except Exception as e: 
        # If any other exception occurs, exit the program
        sys.exit(f"Error: {e}") 
    return users







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













def get_videos_request(username):
    global access_token, post_requests

    # Declare the hashtags list
    all_hashtags =  set()

    # Calulate the date range for the query (The end_date must be no more than 30 days after the start_date)
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    end_date_string = end_date.strftime('%Y%m%d')    
    start_date_string = start_date.strftime('%Y%m%d')


    # Set the url, with the fields we want to retrieve -> id, username, hashtag_names
    url = 'https://open.tiktokapis.com/v2/research/video/query/?fields=id,username,hashtag_names'   
    

    # Set the header
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }


    
    # Set the body
    body = {
        "query": {
            "and": [
                {
                    "operation": "EQ",
                    "field_name": "username",
                    "field_values": [username]
                },
            ],
        },
        "max_count": 100,
        "start_date": start_date_string,
        "end_date": end_date_string,
    }


    
    # Get response
    response = requests.post(url=url, headers=headers, json=body)
    post_requests += 1


    # Check request status code
    if response.status_code == 200:
        data = response.json().get('data')

        videos = data.get('videos')
        for video in videos:
            # Extra check: if the exact username is not found it returns users with 'username' inside
            # example: for username = "user1" it returns also ("user1.dea", "hello.user1")
            tmp = video.get('username')
            if tmp == username:
                # Checker that the hashtag list is not empty
                if 'hashtag_names' in video:
                    all_hashtags.update(video['hashtag_names'])
        
    elif response.status_code == 401:
        # If status code 401, means the access token it's incorrect, terminate program and try again
        print("Status code 401 Unauthorized: The request has not been applied because it lacks valid authentication credentials for the target resource.")
        sys.exit("Terminating the program due to an error. Please check your access credentials")
    elif response.status_code == 500:
        # Internal Server Error: This indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
        return
    elif response.status_code == 429:
        # Reached daily limit
        # Try fetching again the username by re-appending it in the queue
        print("Daily quota limit exceeded. Status code:", response.status_code, response.text)
        users_queue.append(username)
        return
    else:
        print("Failed to retrieve videos. Status code:", response.status_code, response.text)
        return
    
    return list(all_hashtags)







def fetch_range_hashtags():
    global post_requests, users_queue, hashtags_list

    # Loop until queue is empty
    while users_queue:
        if(post_requests < 900): # the daily limit is a 1000 requests per day
            # Get the first item from the queue
            i = users_queue.pop(0)

            # Get the hashtags list of that user
            hashtags_tmp = get_videos_request(i)

            # Add the newly fetched hashtasg to the global hashtags_list
            hashtags_list.extend(hashtags_tmp)

            # Add the user with it's corresponding hashtags in the global users_hashtags_dict
            users_hashtags_dict[i] = hashtags_tmp
        else:
            print("Rate limit reached. Going to sleep until reset at 12 AM UTC.")
            current_time = datetime.datetime.utcnow()
            reset_time = datetime.datetime.combine(current_time.date() + datetime.timedelta(days=1), datetime.time(0))
            sleep_seconds = (reset_time - current_time).total_seconds()
            print(f"Current time: {current_time}, Reset time: {reset_time}, Sleep for {sleep_seconds} seconds")
            time.sleep(sleep_seconds)
            post_requests = 0  # Reset the request counter after sleep









########## Declaring Global Variables ##########
access_token = None
key = None
secret = None
post_requests = 0



########## Declaring Global Data Structures ##########
users_queue = []    # Queue of users to fetch
hashtags_list = []  # Hashtags retrieved up to that point
users_hashtags_dict = {}    # Dictionary of hashtags per user









def main_query(stdin_key, stdin_secret, file_path):
    # Set saving options
    atexit.register(cleanup_and_save)
    signal.signal(signal.SIGINT, handle_signal_received)
    signal.signal(signal.SIGTERM, handle_signal_received)


    try:
        global key, secret
        key = stdin_key
        secret = stdin_secret


        ##### Start the thread to create the access tokens #####
        # Create a thread that will execute the create_tokens function
        # Daemon threads are stopped automatically when the main program exits
        # Start the thread
        threading.Thread(target=create_tokens, daemon=True).start()

        # Wait for the first access token to be available
        wait_for_token()

        # For debugging purposes
        print(f"Parsing: {file_path}")


        # Get all the users to parse from the file
        starting_users = read_from_csv(file_path)

        # Add all starting users to the data structures
        for user in starting_users:
            users_queue.append(user)
        
        
        print("Queue complete, starting fetching")


        fetch_range_hashtags()
        cleanup_and_save()
    except Exception as e:
        # If exception is catched save and close
        cleanup_and_save()
        print(f"Unhandled exception: {e}")






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate user queries with provided credentials.")

    parser.add_argument("key", help="API key for authentication.")
    parser.add_argument("secret", help="API secret for authentication.")
    parser.add_argument("file_path", help="Path to the usernames input or a single username. Ends with .csv for list input.")

    args = parser.parse_args()

    # Set global variables
    key = args.key
    secret = args.secret
    file_path = args.file_path


    main_query(key, secret, file_path)


   


