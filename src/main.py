
import user_following_query
import create_access_token



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




# Switch case block function, actual block is from python 3.10 above
def switch(option, user_input, token):
    if option == "User Following Query":
        if user_input == "Type one starting username":
            user_following_query.parse_with_stdin(token)
        else:
            user_following_query.parse_with_list(token)
        return


        




def main():
    print("\n")

    # Choose which service to provide 
    print("Please choose what service you would like to access:")
    service_options = ["User Following Query", "User Liked Videos Query"]
    service_chose = get_user_choice(service_options)

    print("\n")

    # Choose if from stdin or from list
    print("Please choose how to upload the usernames to be parsed")
    user_input_options = ["Type one starting username", "Upload a list"]
    user_input = get_user_choice(user_input_options)

    print("\n")

    # Get key and secret
    key = input("Please enter your key (don't worry this information wont be saved): ")
    secret = input("Please enter your secret (don't worry this information wont be saved): ")






    # Create the access token
    access_token = create_access_token.get_token(key, secret)

    switch(service_chose, user_input, access_token)





if __name__ == "__main__":
    main()