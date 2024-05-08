import argparse
import csv
import os
import sys

import pandas as pd
import igraph as ig
import numpy as np
import helpers.backboning as bk
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

    q1 = p25
    q2 = p50
    q3 = p75


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




    x_min = q1 - (q3 - q1) * 0.25  # Less padding on the left
    x_max = q3 + (q3 - q1) * 0.25  # Less padding on the right

    # Plot histogram of scores
    plt.figure(figsize=(10, 6))
    bins = np.linspace(x_min, x_max, 30)  # Adjust bins to match new x-axis limits
    plt.hist(scores, bins=bins, color='blue', alpha=0.7)
    plt.title('Distribution of PageRank Scores')
    plt.xlabel('PageRank Score')
    plt.ylabel('Frequency (Log Scale)')
    plt.yscale('log')

    plt.axvline(q1, color='r', linestyle='dashed', linewidth=1, label='Q1')
    plt.axvline(q2, color='g', linestyle='dashed', linewidth=1, label='Median (Q2)')
    plt.axvline(q3, color='b', linestyle='dashed', linewidth=1, label='Q3')

    plt.xlim(x_min, x_max)  # Apply new limits

    plt.legend()
    plt.grid(True)
   
    # Save the plot to a file
    plt.savefig('./pagerank_distribution.png')

    # Optionally, close the plot to free up memory
    plt.close()


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




def backboning(input_path, output_path, threshold):
    table, nnodes, nnedges = bk.read(input_path, "weight")
    nc_table = bk.noise_corrected(table)
    nc_backbone = bk.thresholding(nc_table, threshold)
    bk.write(nc_table, f'network_table_{threshold}', "nc", output_path)
    bk.write(nc_backbone, f'network_backbone_{threshold}', "nc", output_path)




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
    # print(components)
    # print('\n')

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
    for i in range(10, 101, 10):
        threshold = i
        backboning("./weighted_network.tsv", "./backboning_outputs", threshold)


    # Get values for the plots
    edges_sizes = []
    gcc_sizes = []
    for i in range(10, 101, 10):
        threshold = i
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
def louvain_main(filepath):  
    # Get the edges
    edges = read_from_tsv(filepath)

    # Create the graph
    g = ig.Graph.TupleList(edges, directed=False, edge_attrs=['weight'])

    # Find communities
    louvain_communities = g.community_multilevel()

    # Prints
    print(louvain_communities)
    print('\n')
    print("Modularity:", louvain_communities.modularity)
    print("Number of communities:", len(louvain_communities))
    print('\n\n\n')
    print("Community sizes:", louvain_communities.sizes())
    # print("Membership:", louvain_communities.membership)



    communities_with_sizes = [(i + 1, community, size) for i, (community, size) in enumerate(zip(louvain_communities, louvain_communities.sizes()))]
    communities_sorted_by_size = sorted(communities_with_sizes, key=lambda x: x[2], reverse=True)
    print("Sorted community sizes with members:")
    for num, community, size in communities_sorted_by_size:
        print(f"Community {num} ({size} members)")
        

    # Writing the communities to a CSV file
    with open('community_memberships.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Community ID', 'Nodes'])
        # Iterate over each community and get the nodes it contains
        for idx, community in enumerate(louvain_communities):
            # Convert node indices to string and join with commas
            nodes_names = ', '.join(g.vs[node]['name'] for node in community)
            writer.writerow([idx, nodes_names])



    # Add community ID as an attribute to each node
    g.vs['community'] = louvain_communities.membership

    # Export graph to GraphML
    g.write_graphml('network_with_communities.graphml')
    
   
    print("Program ended succesfully")






# louvain_main("./Simple_Network_TSV.tsv")






if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("network_path")

    args = parser.parse_args()

    pageranking_main(args.network_path)


