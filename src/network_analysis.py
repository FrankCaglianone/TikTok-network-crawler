import argparse
import csv
import os
import sys
import igraph as ig
import numpy as np
import helpers.backboning as backboning
import matplotlib.pyplot as plt


import save_files









def plot(g):
    g.vs["label"] = g.vs["name"]
    fig, ax = plt.subplots()
    ig.plot(
        g,
        target=ax,
        # layout="sugiyama",
        vertex_size=15,
        vertex_color="blue",
        edge_color="#222",
        edge_width=1,
    )
    plt.show()







#################### PAGERANKING ####################

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
                


def calculate_and_save_pageranks(g):

    # Calculate the page ranking with damping factor of 0.85
    pagerank = g.pagerank(damping=0.85)


    # Pair ranks with usernames
    pagerank_list = []
    for vertex, score in zip(g.vs, pagerank):
        pagerank_list.append((vertex['name'], score))


    # Sort the list in ascending order
    sorted_pageranks_list = sorted(pagerank_list, key=lambda item: item[1])


    # TODO: Give proper comment
    scores = [score for name, score in sorted_pageranks_list]


    # Calculate percentiles
    p25 = np.percentile(scores, 25)
    p50 = np.percentile(scores, 50)
    p75 = np.percentile(scores, 75)


    min_score = np.min(scores)  # 0th percentile
    max_score = np.max(scores)  # 100th percentile


    # Initialize lists for each range
    range_0_25 = []
    range_26_50 = []
    range_51_75 = []
    range_76_100 = []


    # Assign tuples to each range based on their Page Rank
    for name, score in sorted_pageranks_list:
        if score <= p25:
            range_0_25.append((name, score))
        elif p25 < score <= p50:
            range_26_50.append((name, score))
        elif p50 < score <= p75:
            range_51_75.append((name, score))
        elif score > p75:
            range_76_100.append((name, score))


    # Save the results in .csv format
    save_files.save_25_percentile(range_0_25, min_score, p25)
    save_files.save_50_percentile(range_26_50, p25, p50)
    save_files.save_75_percentile(range_51_75, p50, p75)
    save_files.save_100_percentile(range_76_100, p75, max_score)


    print("All percentiles .csv saved!")



def pageranking_main(path):
    # Read the .csv
    network = read_network(path)

    # Create the graph from the list of edges
    graph = ig.Graph.TupleList(network, directed=True)
    
    # Calculate the page rankings and save the results in quartiles
    calculate_and_save_pageranks(graph)

    print("Program ended succesfully")




















#################### BACKBONING ####################

def write_tsv_weighted_network(network):
    modified_list = [(t[0], t[1], 1) for t in network]

    # Write the modified list to a .tsv file
    with open('weighted_network.tsv', 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        writer.writerow(["src", "trg", "weight"])
        writer.writerows(modified_list)




def backboning_func(input_path, output_path, threshold):
    table, nnodes, nnedges = backboning.read(input_path, "weight")
    nc_table = backboning.noise_corrected(table)
    nc_backbone = backboning.thresholding(nc_table, threshold)
    backboning.write(nc_table, f'network_table_{threshold}', "nc", output_path)
    backboning.write(nc_backbone, f'network_backbone_{threshold}', "nc", output_path)





def read_from_tsv(path):
    edges = []
    with open(path, 'r') as file:
        next(file) # Skip the header
        for line in file:
            parts = line.strip().split('\t')
            source = parts[0]
            destination = parts[1]
            weight = int(parts[2])
            edges.append((source, destination, weight))
    return edges




def get_plots_values(filepath):
    # Get the edges
    edges = read_from_tsv(filepath)


    # Create the graph
    g = ig.Graph.TupleList(edges, directed=False, edge_attrs=['weight'])


    # Calculate the number of edges
    edges_sizes = len(edges)


    # Find the weakly connected components
    components = g.connected_components(mode="weak")
    print(components)
    print('\n')

    # Get the Giant Weekly connected component
    gcc = 0
    for x in components:
        if len(x) > gcc:
            gcc = len(x)


    return edges_sizes, gcc







def backboning_main(path):
    # Read the .csv
    network = read_network(path)

    # Create the .tsv file for the backboning function
    write_tsv_weighted_network(network)


    # Check if the directory exists, otherwise create one
    output_dir = './backboning_outputs'
    if not os.path.exists(output_dir):
        # Create the directory if it does not exist
        os.makedirs(output_dir)


    # Backboning for various thresholds and saving the results
    for i in range(1, 11):
        threshold = i / 10.0
        backboning("./weighted_network.tsv", "./backboning_outputs", threshold)


    # Get values for the plots
    edges_sizes = []
    gcc_sizes = []
    for i in range(10):
        threshold = i / 10.0
        size, gcc = get_plots_values(f'./backboning_outputs/network_backbone_{threshold}_nc.csv')
        edges_sizes.append(size)
        gcc_sizes.append(gcc)

    
    print('\n')
    print('\n')
    print('\n')
    print('\n')
    print("Edge Sizes: ", edges_sizes)
    print("GCC Sizes: ", gcc_sizes)


    # Create the plots
    # Il primo plot avrà sull'asse x i valori di A e sull'asse y il numero di edges (E(G(Ai))).
    # Il secondo plot avrà sull'asse x i valori di A e sull'asse y la size della giant weakly connected component (GCC_size(G(Ai))).


    print("Program ended succesfully")









    





#################### COMMUNITY DETECTION ####################





def louvain_main():
    # TODO: Community Detection
    # g = ig.Graph.Famous('Zachary')

    # louvain_communities = g.community_multilevel()

    # print(louvain_communities)
    # print("Modularity:", louvain_communities.modularity)
    # print("Membership:", louvain_communities.membership)

   
    print("Program ended succesfully")














# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()

#     parser.add_argument("network_path")

#     args = parser.parse_args()

#     main(args.network_path)


