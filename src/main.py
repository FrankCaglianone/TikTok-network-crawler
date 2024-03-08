
import user_following_query
import create_access_token
import threading
import time



def get_user_choice(options):
    # Print all the options to the user
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    
    while True:
        try:
            # Ask the user for their choice
            user_input = int(input("Enter the number of your choice: "))
            
            # Check if the choice is valid
            if 1 <= user_input <= len(options):
                # Print the chosen option
                chosen_option = options[user_input - 1]
                print(f"You chose: {chosen_option}")
                return chosen_option
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            # Handle non-integer inputs
            print("Please enter a valid number.")




### Global Variables
access_token = None
key = None
secret = None




# Use multithreading to instantiate a timer to create an access token every ~ 2 hours
def create_tokens():
    # Access Global Variables
    global access_token
    global key
    global secret

    while True:
        access_token = create_access_token.get_token(key, secret)
        print(f"New Key Created: {access_token} \n")
        time.sleep(10) # Sleep for 2 hours, 7200s







def main():
    print("\n")

    # Choose which service to provide 
    print("Please choose what service you would like to access:")
    service_options = ["User Following Query", "User Liked Videos Query"]
    service = get_user_choice(service_options)

    print("\n")

    # Choose if from stdin or from list
    print("Please choose how to upload the usernames to be parsed")
    user_input_options = ["Type one starting username", "Upload a list"]
    user_input = get_user_choice(user_input_options)

    print("\n")

    # Get key and secret
    global key 
    global secret
    key = input("Please enter your key (don't worry this information wont be saved): ")
    secret = input("Please enter your secret (don't worry this information wont be saved): ")



    ##### Start the thread to create the access tokens #####
    # Create a thread that will execute the create_tokens function
    thread = threading.Thread(target=create_tokens)
    # Daemon threads are stopped automatically when the main program exits
    thread.daemon = True
    # Start the thread
    thread.start()




    global access_token


    if service == "User Following Query":
        if user_input == "Type one starting username":
            user_following_query.parse_with_stdin(access_token)
        else:
            user_following_query.parse_with_list(access_token)
        return
    



main()




# if __name__ == "__main__":
#     main()