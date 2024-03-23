import user_following_query
import create_access_token
import threading
import time
import argparse



# def get_user_choice(options):
#     # Print all the options to the user
#     for i, option in enumerate(options, start=1):
#         print(f"{i}. {option}")
    
#     while True:
#         try:
#             # Ask the user for their choice
#             user_input = int(input("Enter the number of your choice: "))
            
#             # Check if the choice is valid
#             if 1 <= user_input <= len(options):
#                 # Print the chosen option
#                 chosen_option = options[user_input - 1]
#                 print(f"You chose: {chosen_option}")
#                 return chosen_option
#             else:
#                 print(f"Please enter a number between 1 and {len(options)}.")
#         except ValueError:
#             # Handle non-integer inputs
#             print("Please enter a valid number.")






# def main():
#     # Access all global variables
#     global key, secret, access_token

#     print("\n")

#     # Choose which service to provide 
#     print("Please choose what service you would like to access:")
#     service_options = ["User Following Query", "User Liked Videos Query"]
#     service = get_user_choice(service_options)

#     print("\n")

#     # Choose if from stdin or from list
#     print("Please choose how to upload the usernames to be parsed")
#     user_input_options = ["Type one starting username", "Upload a list"]
#     user_input = get_user_choice(user_input_options)

#     print("\n")

#     # Get key and secret
#     key = input("Please enter your key (don't worry this information wont be saved): ")
#     secret = input("Please enter your secret (don't worry this information wont be saved): ")


#     ##### Start the thread to create the access tokens #####
#     # Create a thread that will execute the create_tokens function
#     # Daemon threads are stopped automatically when the main program exits
#     # Start the thread
#     threading.Thread(target=create_tokens, daemon=True).start()


#     # Wait for the first access token to be available
#     wait_for_token()


#     # Based on the users options start the parsing
#     if service == "User Following Query":
#         if user_input == "Type one starting username":
#             user_following_query.parse_with_stdin(access_token)
#         else:
#             user_following_query.parse_with_list(access_token)
#         return













### Global Variables
access_token = None
key = None
secret = None
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
        time.sleep(7000) # Sleep for 2 hours, 7200s




# Wait for the access token to be available.
def wait_for_token():
    global access_token
    with condition:
        while access_token is None:
            condition.wait()  # Wait until the access token is updated




    

def main(user_input):
    # Access all global variables
    global key, secret, access_token

    ##### Start the thread to create the access tokens #####
    # Create a thread that will execute the create_tokens function
    # Daemon threads are stopped automatically when the main program exits
    # Start the thread
    threading.Thread(target=create_tokens, daemon=True).start()

    # Wait for the first access token to be available
    wait_for_token()

    # Determine how to handle user input based on the file extension
    if user_input.endswith('.csv'):
        user_following_query.parse_with_list(access_token, user_input)
    else:
        user_following_query.parse_with_stdin(access_token, user_input)






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate user queries with provided credentials.")

    parser.add_argument("key", help="API key for authentication.")
    parser.add_argument("secret", help="API secret for authentication.")
    parser.add_argument("user_input", help="Path to the usernames input or a single username. Ends with .csv for list input.")

    args = parser.parse_args()

    # Set global variables
    key = args.key
    secret = args.secret

    # Call the main function with the appropriate service and input path
    main(args.user_input)

