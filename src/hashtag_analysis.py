import argparse
import ast
import csv
import sys
from collections import Counter

import save_files as sv






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



def extract_hashtag_occurencies(file_path):
    occurencies = []

    try:
       with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Read the header row
            
            # Iterate over each row in the CSV
            for row in reader:
                occurencies.append(row[0])

    except FileNotFoundError:
        # If the file is not found, print an error message and exit the program
        sys.exit(f"Error: The file at {file_path} was not found.") 
    except Exception as e: 
        # If any other exception occurs, exit the program
        sys.exit(f"Error: {e}") 
    
    return occurencies





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


    






def calculate_percentile_frequency(users_list, hash_dict, output_name):

    hashtags = []

    for usr in users_list:
        if usr in hash_dict:
            hashtags.extend(hash_dict[usr])
        else:
            print(f"ERROR 404: user '{usr}' not found ")

    

    occurencies = Counter(hashtags)

    # Sort the occurrences by frequency in descending order
    sorted_occurrences = sorted(occurencies.items(), key=lambda item: item[1], reverse=True)

    # Save to .csv format
    sv.save_quartile_hashtags(sorted_occurrences, output_name)


    # Print each element and its frequency
    # for element, count in sorted_occurrences:
    #     print(element, count)
    








def calulate_communities_frequency(users_list, hash_dict, output_name):

    hashtags = []

    for usr in users_list:
        if usr in hash_dict:
            hashtags.extend(hash_dict[usr])
        else:
            print(f"ERROR 404: user '{usr}' not found ")
    

    occurencies = Counter(hashtags)

    # Sort the occurrences by frequency in descending order
    sorted_occurrences = sorted(occurencies.items(), key=lambda item: item[1], reverse=True)

    # Save to .csv format
    sv.save_communities_hashtags(sorted_occurrences, output_name)


    # Print each element and its frequency
    # for element, count in sorted_occurrences:
    #     print(element, count)






    





def main_quartile_hashtag_analysis(hashtags_path, Q1_path, Q2_path, Q3_path, Q4_path,):
    # Fetch all the hashtags as dictionary username = list(hashtags)
    hashtags_dict = extract_hashtags_from_csv(hashtags_path)

    # Fetch quartiles users
    Q1_users = extract_quartile_users(Q1_path)
    Q2_users = extract_quartile_users(Q2_path)
    Q3_users = extract_quartile_users(Q3_path)
    Q4_users = extract_quartile_users(Q4_path)

    # Calculate frequency for quartiles
    calculate_percentile_frequency(Q1_users, hashtags_dict, "q1")
    calculate_percentile_frequency(Q2_users, hashtags_dict, "q2")
    calculate_percentile_frequency(Q3_users, hashtags_dict, "q3")
    calculate_percentile_frequency(Q4_users, hashtags_dict, "q4")

    print("Program ended succesfully")











def main_community_hashtag_analysis(hashtags_path, communities_path):
    # Fetch all the hashtags as dictionary username = list(hashtags)
    hashtags_dict = extract_hashtags_from_csv(hashtags_path)

    # Fetch communities
    communities = extract_communities(communities_path)

    for community in communities:
        calulate_communities_frequency(communities[community], hashtags_dict, f"community_{community}")







def tf_idf_pageranking(Q1_path, Q2_path, Q3_path, Q4_path):
    
   # Extract hashtag occurrences for each query
    q1 = extract_hashtag_occurencies(Q1_path)
    q2 = extract_hashtag_occurencies(Q2_path)
    q3 = extract_hashtag_occurencies(Q3_path)
    q4 = extract_hashtag_occurencies(Q4_path)
    
    # Convert dictionaries to sets of keys for easier comparison
    q1_set = set(q1)
    q2_set = set(q2)
    q3_set = set(q3)
    q4_set = set(q4)
    

    hashtag_counter = {}
    for hashtag_set in (q1_set, q2_set, q3_set, q4_set):
        for hashtag in hashtag_set:
            if hashtag in hashtag_counter:
                hashtag_counter[hashtag] += 1
            else:
                hashtag_counter[hashtag] = 1
    
    # Determine which hashtags appear in at least two dictionaries
    common_hashtags = {hashtag for hashtag, count in hashtag_counter.items() if count >= 2}
    
    # Remove common hashtags from each dictionary
    for hashtag in common_hashtags:
        q1.pop(hashtag)
        q2.pop(hashtag)
        q3.pop(hashtag)
        q4.pop(hashtag)
    

    
    sv.save_quartile_hashtags(q1, "tf_idf_q1")
    sv.save_quartile_hashtags(q2, "tf_idf_q2")
    sv.save_quartile_hashtags(q3, "tf_idf_q3")
    sv.save_quartile_hashtags(q4, "tf_idf_q4")




    

    



    






if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # parser.add_argument("hashtags_path")


    # For quartiles
    parser.add_argument("Q1_path")
    parser.add_argument("Q2_path")
    parser.add_argument("Q3_path")
    parser.add_argument("Q4_path")
    
    

    # For communities
    # parser.add_argument("communities_path")




    args = parser.parse_args()



    # For quartiles
    # main_quartile_hashtag_analysis(args.hashtags_path, args.Q1_path, args.Q2_path, args.Q3_path, args.Q4_path)

    # For communities
    # main_community_hashtag_analysis(args.hashtags_path, args.communities_path)

    tf_idf_pageranking(args.Q1_path, args.Q2_path, args.Q3_path, args.Q4_path)
   









