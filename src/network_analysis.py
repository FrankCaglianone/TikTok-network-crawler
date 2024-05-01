import argparse
import csv
import sys
import igraph as ig
import numpy as np
import helpers.backboning as backboning
import matplotlib.pyplot as plt
import networkx as nx

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

    # Debugging
    print("All percentiles .csv saved!")

    





def backboning_func(input_path, output_path):
    table, nnodes, nnedges = backboning.read(input_path, "weight")
    nc_table = backboning.noise_corrected(table)
    nc_backbone = backboning.thresholding(nc_table, 0.05)
    backboning.write(nc_backbone, "tiktok_backboning_network", "nc", output_path)




    





def main(network_path, weighted_network):

    # Read the .csv
    network = read_network(network_path)

    # Create the graphs from the list of edges
    directed_graph = ig.Graph.TupleList(network, directed=True)
    undirected_graph = ig.Graph.TupleList(network, directed=False)
    

    # Calculate the page rankings and save in quartiles
    # calculate_and_save_pageranks(directed_graph)


    # TODO: Backboning
    # backboning_func(weighted_network, "./")


    # TODO: Community Detection
    g = ig.Graph.Famous('Zachary')
    louvain_communities = g.community_multilevel()

    print(louvain_communities)
    print("Modularity:", louvain_communities.modularity)
    print("Membership:", louvain_communities.membership)



   
    # print("Program ended succesfully")




main("./Simple_Network.csv", "ciao")





# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()

#     parser.add_argument("network_path")

#     args = parser.parse_args()

#     main(args.network_path)


