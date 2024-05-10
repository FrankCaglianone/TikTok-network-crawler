import argparse
import ast
import csv
import os
import sys
import pandas as pd
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
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Convert the DataFrame to a dictionary
    hashtag_dict = dict(zip(data['Hashtag'], data['Frequency']))

    return hashtag_dict



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







def remove_common_strings(*dicts):
    # Find common keys in all dictionaries
    common_keys = set(dicts[0].keys())  # Start with keys from the first dictionary
    for d in dicts[1:]:  # Iterate over the rest of the dictionaries
        common_keys.intersection_update(d.keys())

    # Remove common keys from all dictionaries
    for key in common_keys:
        for d in dicts:
            d.pop(key, None)

    return dicts





def remove_common_in_two_or_more(*dicts):
    from collections import Counter

    # Count all occurrences of each key across all dictionaries
    key_count = Counter(key for d in dicts for key in d.keys())

    # Identify keys that appear in two or more dictionaries
    keys_to_remove = {key for key, count in key_count.items() if count >= 2}

    # Remove these keys from all dictionaries
    for key in keys_to_remove:
        for d in dicts:
            d.pop(key, None)

    return dicts





def remove_common_keys(dicts):
    # Find common keys in all dictionaries
    common_keys = set(dicts[0].keys())  # Start with keys from the first dictionary
    for d in dicts[1:]:  # Iterate over the rest of the dictionaries
        common_keys.intersection_update(d.keys())


    # Remove common keys from all dictionaries
    for key in common_keys:
        for d in dicts:
            d.pop(key, None)
    return dicts




def tf_idf_pageranking(Q1_path, Q2_path, Q3_path, Q4_path):
    
   # Extract hashtag occurrences for each query
    q1 = extract_hashtag_occurencies(Q1_path)
    q2 = extract_hashtag_occurencies(Q2_path)
    q3 = extract_hashtag_occurencies(Q3_path)
    q4 = extract_hashtag_occurencies(Q4_path)
    
    updated_dicts = remove_common_strings(q1, q2, q3, q4)


    # Save each dictionary to a separate CSV file
    for i, d in enumerate(updated_dicts):
        # Convert dictionary to a list of dictionaries suitable for DataFrame creation
        data_list = [{'Hashtag': hashtag, 'Frequency': frequency} for hashtag, frequency in d.items()]
        
        # Create DataFrame
        df = pd.DataFrame(data_list)

        # Save the DataFrame to a CSV file
        csv_file_path = f'updated_data_{i+1}.csv'
        df.to_csv(csv_file_path, index=False)
        
        print(f'Data saved to {csv_file_path}.')

    



def tf_idf_communities(path):
    # Directory to save the updated CSV files
    save_directory = './tfidf_communities_hashtags'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # dicts = []
    # for i in range(38):
    #     file_path = f"{path}{i}.csv"
    #     dicts.append(extract_hashtag_occurencies(file_path))    


    file0 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_0.csv")
    file1 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_1.csv")
    file2 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_2.csv")
    file3 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_3.csv")
    file4 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_4.csv")
    file5 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_5.csv")
    file6 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_6.csv")
    file7 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_7.csv")
    file8 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_8.csv")
    file9 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_9.csv")
    file10 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_10.csv")
    file11 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_11.csv")
    file12 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_12.csv")
    file13 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_13.csv")
    file14 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_14.csv")
    file15 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_15.csv")
    file16 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_16.csv")
    file17 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_17.csv")
    file18 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_18.csv")
    file19 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_19.csv")
    file20 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_20.csv")
    file21 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_21.csv")
    file22 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_22.csv")
    file23 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_23.csv")
    file24 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_24.csv")
    file25 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_25.csv")
    file26 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_26.csv")
    file27 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_27.csv")
    file28 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_28.csv")
    file29 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_29.csv")
    file30 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_30.csv")
    file31 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_31.csv")
    file32 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_32.csv")
    file33 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_33.csv")
    file34 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_34.csv")
    file35 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_35.csv")
    file36 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_36.csv")
    file37 = extract_hashtag_occurencies("./communities_hashtags_outputs/community_37.csv")


        
    # Remove common strings
    # We need to unpack the list of dictionaries as separate arguments
    # updated_dicts = remove_common_strings(*dicts)
    updated_dicts = remove_common_in_two_or_more(file0, file1, file2, file3, file4, file5, file6, file7, file8, file9, file10, file11, file12, file13, file14, file15, file16, file17, file18, file19, file20, file21, file22, file23, file24, file25, file26, file27, file28, file29, file30, file31, file32, file33, file34, file35, file36, file37)

    
    # Save each dictionary to a separate CSV file
    for i, d in enumerate(updated_dicts):
        # Convert dictionary to a list of dictionaries suitable for DataFrame creation
        data_list = [{'Hashtag': hashtag, 'Frequency': frequency} for hashtag, frequency in d.items()]
        
        # Create DataFrame
        df = pd.DataFrame(data_list)
        # Save the DataFrame to a CSV file
        csv_file_path = os.path.join(save_directory, f'tfidf_community_{i}.csv')
        df.to_csv(csv_file_path, index=False)
        
        print(f'Data saved to {csv_file_path}.')


    






if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("hashtags_path")


    # For quartiles
    # parser.add_argument("Q1_path")
    # parser.add_argument("Q2_path")
    # parser.add_argument("Q3_path")
    # parser.add_argument("Q4_path")
    
    

    # For communities
    # parser.add_argument("communities_path")




    args = parser.parse_args()
    tf_idf_communities(args.hashtags_path)





    # For quartiles
    # main_quartile_hashtag_analysis(args.hashtags_path, args.Q1_path, args.Q2_path, args.Q3_path, args.Q4_path)

    # For communities
    # main_community_hashtag_analysis(args.hashtags_path, args.communities_path)

    # tf_idf_pageranking(args.Q1_path, args.Q2_path, args.Q3_path, args.Q4_path)
   



