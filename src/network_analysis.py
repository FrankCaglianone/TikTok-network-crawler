import argparse
import csv
import sys
import igraph as ig
import numpy as np
import matplotlib.pyplot as plt

import save_files



# Helper function
def print_page_ranks(graph, pagerank):
    print("PageRank Scores:")
    for vertex, score in zip(graph.vs, pagerank):
        print(f"{vertex['name']}: {score:.4f}")



def print_nodes_list(graph):
    print("List of nodes:")
    for v in graph.vs:
        print(f"Node ID: {v.index}, Name: {v['name']}")








# g.vs["label"] = g.vs["name"]


# fig, ax = plt.subplots()
# ig.plot(
#     g,
#     target=ax,
#     # layout="sugiyama",
#     vertex_size=15,
#     vertex_color="blue",
#     edge_color="#222",
#     edge_width=1,
# )
# plt.show()
















def read_from_csv(file_path):
    # Initialize an empty list to store edges
    edges = []

    try:
        # Read the CSV file
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                edges.append(tuple(row))
    except FileNotFoundError:
        # If the file is not found, print an error message and exit the program
        sys.exit(f"Error: The file at {file_path} was not found.") 
    except Exception as e: 
        # If any other exception occurs, exit the program
        sys.exit(f"Error: {e}") 
    return edges







def calculate_and_save_pageranks(g):

    # Calculate the page ranking
    # TODO: pagerank = g.pagerank(damping=0.85)?
    pagerank = g.pagerank()


    # Pair ranks with usernames
    pagerank_list = []
    for vertex, score in zip(g.vs, pagerank):
        pagerank_list.append((vertex['name'], score))


    # Sort the list
    # TODO: ascending or descending? -> # sorted_scores = sorted(pageranks_map.items(), key=lambda item: item[1], reverse=True)
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

    print("Program ended succesfully")

    





def main(file_path):

    edges = read_from_csv(file_path)

    # Create a graph from the list of edges
    graph = ig.Graph.TupleList(edges, directed=True)

    calculate_and_save_pageranks(graph)






# './Sample_User_Network.csv'



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("file_path")

    args = parser.parse_args()

    main(args.file_path)


