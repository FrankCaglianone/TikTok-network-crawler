import ast
import csv
import sys






def extract_hashtags_from_csv(file_path):
    # Initialize a dictionary to store the data
    hashtags_dict = {}
    
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Read the header row
        
            # Iterate over each row in the CSV
            for row in reader:
                if row[0] and row[1]:  # Ensure the necessary data is present
                    username = row[0]
                    # Evaluate the hashtags string as a list
                    hashtags = ast.literal_eval(row[1].strip())
                    # Add to dictionary
                    hashtags_dict[username] = hashtags
    except FileNotFoundError:
        # If the file is not found, print an error message and exit the program
        sys.exit(f"Error: The file at {file_path} was not found.") 
    except Exception as e: 
        # If any other exception occurs, exit the program
        sys.exit(f"Error: {e}") 

    return hashtags_dict






def extract_quartile_users(file_path):
    users = []

    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Read the header row
            
            # Iterate over each row in the CSV
            for row in reader:
                users.append(row[0])
    except FileNotFoundError:
        # If the file is not found, print an error message and exit the program
        sys.exit(f"Error: The file at {file_path} was not found.") 
    except Exception as e: 
        # If any other exception occurs, exit the program
        sys.exit(f"Error: {e}") 
    
    return users









def extract_communities(file_path):
    # Initialize a dictionary to store the data
    communities = {}
    
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Read the header row
        
            # Iterate over each row in the CSV
            for row in reader:
                if row[0] and row[1]:  
                    community = row[0]
                    # Evaluate the hashtags string as a list
                    users = [tag.strip() for tag in row[1].split(',')]
                    # Add to dictionary
                    communities[community] = users
    except FileNotFoundError:
        # If the file is not found, print an error message and exit the program
        sys.exit(f"Error: The file at {file_path} was not found.") 
    except Exception as e: 
        # If any other exception occurs, exit the program
        sys.exit(f"Error: {e}") 

    return communities


    










def calculate_frequency():
    print()







def main(hashtags_path, Q1_path, Q2_path, Q3_path, Q4_path, communities_path):
    # Fetch all the hashtags as dictionary username = list(hashtags)
    hashtags_dict = extract_hashtags_from_csv(hashtags_path)

    # Fetch quartiles users
    Q1_users = extract_quartile_users(Q1_path)
    Q2_users = extract_quartile_users(Q2_path)
    Q3_users = extract_quartile_users(Q3_path)
    Q4_users = extract_quartile_users(Q4_path)

    # Fetch communities
    communities = extract_communities(communities_path)








extract_communities("./community_memberships.csv")
   
   





