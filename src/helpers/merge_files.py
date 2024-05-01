import argparse
import csv





def read_dict_csv(filename):

    # Dictionary to store the data
    user_status_dict = {}

    # Read the CSV file
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        for row in reader:
            if row:  # Check if row is not empty
                username = row[0].strip()  # Remove any leading/trailing whitespace
                status = int(row[1].strip())  # Convert status to integer
                user_status_dict[username] = status

    
    return user_status_dict






def write_dict_csv(list):
    with open('complete_list.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Parsed Status"])  # Writing headers
            for username, parsed_status in list.items():
                writer.writerow([username, parsed_status])






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






def main(path1, path2):

    # Dictionary execution
    dict1 = read_dict_csv(path1)
    dict2 = read_dict_csv(path2)
    dict1.update(dict2)
    write_dict_csv(dict1)


    # Network execution
    # network1 = read_network_csv(path1)
    # network2  = read_network_csv(path2)
    # network1.extend(network2)
    # write_network_csv(network1)


    print("Program ended succesfully")









if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("file1")
    parser.add_argument("file2")

    args = parser.parse_args()

    main(args.file1, args.file2)