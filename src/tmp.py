import argparse
import csv





def read_csv(filename):

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






def write_csv(list):
    with open('complete_list.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Parsed Status"])  # Writing headers
            for username, parsed_status in list.items():
                writer.writerow([username, parsed_status])




def main(path1, path2):

    dict1 = read_csv(path1)

    dict2 = read_csv(path2)

    dict1.update(dict2)

    write_csv(dict1)







if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("list1")
    parser.add_argument("list2")

    args = parser.parse_args()

    main(args.list1, args.list2)