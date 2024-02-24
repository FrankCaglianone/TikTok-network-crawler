# import user_followers_query
# # user_followers_query.main()



def get_user_choice():
    options = ["User Followers Query", "User Following Query"]

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


        
# Define global variables
service_chose = get_user_choice()