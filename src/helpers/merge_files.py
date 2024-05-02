import argparse
import csv




######### MERGE DICTIONARIES #########
def read_dict_csv(filename):

    # Dictionary to store the data
    user_status_dict = {}

    # Read the CSV file
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        for row in reader:
            if row:  # Check if row is not empty
                username = row[0]
                status = row[1]
                user_status_dict[username] = status

    
    return user_status_dict


def write_dict_csv(list):
    with open('complete_list.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Parsed Status"])  # Writing headers
            for username, parsed_status in list.items():
                writer.writerow([username, parsed_status])





######### MERGE NETWORK TUPLES LISTS #########

def read_network_csv(file_path):
    # List to store the tuples
    data_tuples = []

    # Reading the CSV file
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header
        for row in csv_reader:
            data_tuples.append((row[0], row[1]))  # Append each row as a tuple to the list

    return data_tuples




def write_network_csv(network):
     with open('complete_network.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Source", "Destination"])
        # Write each tuple in the network list to the file
        for connection in network:
            writer.writerow(connection)










######### MERGE VIDEO QUERIES DICTIONARIES #########
def read_users_hashtags(file_path):
    data = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            username, hashtag = row
            data[username] = hashtag
    return data








def write_user_hashtags(dict):
    # Save dictionary to CSV
    with open('complete_user_hashtags.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Hashtags"])  # Writing headers
        for username, hashtag in dict.items():
            writer.writerow([username, hashtag])














def check_for_duplicates(file_path):
    data = []
    duplicates = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            username, hashtag = row
            if username in data:
                duplicates.append(username)
            else:
                data.append(username)
    return duplicates





def check_for_missings(list1, list2):

    # Read from the percentile list
    for username_one in list1:
        
        # Read from video queries
        if username_one in list2:
            continue
        else:
            print(username_one)












def main(path1, path2):

    ##### Dictionary execution #####
    # dict1 = read_dict_csv(path1)
    # dict2 = read_dict_csv(path2)
    # dict1.update(dict2)
    # write_dict_csv(dict1)


    ##### Network execution #####
    # network1 = read_network_csv(path1)
    # network2  = read_network_csv(path2)
    # network1.extend(network2)
    # write_network_csv(network1)



    ##### User hashtags execution #####
    # dict1 = read_users_hashtags(path1)
    # dict2 = read_users_hashtags(path2)

    # merged_data = {}

    # for username, values in dict1.items():
    #     merged_data[username] = values

    # for username, values in dict2.items():
    #     merged_data[username] = values

    # write_user_hashtags(merged_data)




    ##### CHECK FOR DUPLICATES #####
    # print(check_for_duplicates(path1))





    ##### CHECK FOR MISSINGS #####
    dict1 = read_dict_csv(path2) # percentile file
    dict2 = read_users_hashtags(path1) # video query
    check_for_missings(dict1, dict2)



    print("Program ended succesfully")





# main("./complete_user_hashtags_25th.csv", "./25th_percentile.csv")








# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()

#     parser.add_argument("file1")
#     parser.add_argument("file2")

#     args = parser.parse_args()

#     main(args.file1, args.file2)