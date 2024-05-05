import ast
import csv






def extract_hashtags_from_csv(file_path):
    # Initialize a dictionary to store the data
    hashtags_dict = {}
    
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

    return hashtags_dict













    





def extract_quartile():
    print("")





def calculate_frequency():
    print()







def main(hashtags_path):
    # Fetch all the hashtags as dictionary username = list(hashtags)
    hashtags_dict = extract_hashtags_from_csv(hashtags_path)

    

   
   





main("./user_hashtags_1.csv")