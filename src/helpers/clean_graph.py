import argparse
import csv
import os
import sys





def read_parsing_list(path):
    parsing_list = {}

    try:
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header
            for row in reader:
                if row:  # Check if row is not empty
                    username = row[0].strip()  # Remove any leading/trailing whitespace
                    status = int(row[1].strip())  # Convert status to integer
                    parsing_list[username] = status

    except FileNotFoundError:
        # If the file is not found, print an error message and exit the program
        sys.exit(f"Error: The file at {path} was not found.") 
    except Exception as e: 
        # If any other exception occurs, exit the program
        sys.exit(f"Error: {e}") 
    return parsing_list



def read_network(path):
    network = []

    try:
        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header
            for row in csv_reader:
                network.append((row[0], row[1]))  # Append each row as a tuple to the list
                
    except FileNotFoundError:
        # If the file is not found, print an error message and exit the program
        sys.exit(f"Error: The file at {path} was not found.") 
    except Exception as e: 
        # If any other exception occurs, exit the program
        sys.exit(f"Error: {e}") 
    return network
                






def save_cleaned_network(network):
    # If the folder does not exist create one, needed only for the first function to be called out of the 4 ranges functions
    output_dir = 'src/cleaned'
    if not os.path.exists(output_dir):
        # Create the directory if it does not exist
        os.makedirs(output_dir)


    with open('src/cleaned/graph.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Source", "Destination"])
        # Write each tuple in the network list to the file
        for connection in network:
            writer.writerow(connection)



def save_cleaned_nodes(set):
    with open('src/cleaned/cleaned_nodes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Nodes in graph"]) 
        for username in set:
            writer.writerow([username])








def clean_graph(list_path, network_path):

    parsing_list = read_parsing_list(list_path)

    network = read_network(network_path)


    final_graph = []


    # Clean the network excluding edges with nodes that have not been fetched 
    for row in network:
        source, destination = row
        if destination in parsing_list:
            final_graph.append((source, destination))

    

    # Use a set to find all unique nodes
    unique_nodes = set()
    for source, destination in final_graph:
        unique_nodes.update([source, destination])

    
    for username in parsing_list.keys():
        if username not in unique_nodes:
            print(f"User excluded {username}")



    save_cleaned_network(final_graph)
    save_cleaned_nodes(unique_nodes)



    return final_graph








def main(parsing_list, network_list):

    clean_graph(parsing_list, network_list)

    print("Program ended succesfully")








if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("parsing_list")
    parser.add_argument("network_list")

    args = parser.parse_args()

    main(args.parsing_list, args.network_list)