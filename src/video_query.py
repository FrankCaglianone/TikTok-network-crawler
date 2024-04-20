import sys
import threading
import time
import requests
from datetime import date, timedelta

import create_access_token






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







def get_videos(username):
    global access_token

    # Declare the hashtags list
    all_hashtags =  set()

    # Calulate the date and set it to minus 30 days (The end_date must be no more than 30 days after the start_date)
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
        "max_count": 20,
        "start_date": start_date_string,
        "end_date": end_date_string
    }
    
    # Get response
    response = requests.post(url=url, headers=headers, json=body)


    # Check request status code
    if response.status_code == 200:
        videos = response.json().get('data').get('videos')

        for video in videos:
            if 'hashtag_names' in video:
                all_hashtags.update(video['hashtag_names'])

        all_hashtags = list(all_hashtags)

        return all_hashtags
    elif response.status_code == 401:
        # If status code 401, means the access token it's incorrect, terminate program and try again
        print("Status code 401 Unauthorized: The request has not been applied because it lacks valid authentication credentials for the target resource.")
        sys.exit("Terminating the program due to an error. Please check your access credentials")
    elif response.status_code == 500:
        # Internal Server Error: This indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
        return
    else:
        print("Failed to retrieve followers. Status code:", response.status_code)
        return







def main_query(username, stdin_key, stdin_secret):
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


    print(get_videos(username))




