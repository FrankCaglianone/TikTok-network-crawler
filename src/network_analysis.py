import csv
import igraph as ig
import numpy as np
import matplotlib.pyplot as plt



# Helper function
def print_page_ranks():
    print("PageRank Scores:")
    for vertex, score in zip(g.vs, pagerank):
        print(f"{vertex['name']}: {score:.4f}")



def print_nodes_list():
    print("List of nodes:")
    for v in g.vs:
        print(f"Node ID: {v.index}, Name: {v['name']}")





# for name, score in sorted_pageranks_list:
#     print(f"{name}: {score}")





# Extract the 1st quartile



# Search for common words in the 1st quartile


# Search for common words in the 2nd quartile


# Search for common words in the 3rd quartile


# Search for common words in the 4th quartile









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















def calculate_pageranks():

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



    scores = [score for name, score in sorted_pageranks_list]

    # Calculate percentiles
    p25 = np.percentile(scores, 25)
    p50 = np.percentile(scores, 50)
    p75 = np.percentile(scores, 75)

    # Initialize lists for each range
    range_0_25 = []
    range_26_50 = []
    range_51_75 = []
    range_76_100 = []

    # Assign data to each range based on scores
    for name, score in sorted_pageranks_list:
        if score <= p25:
            range_0_25.append((name, score))
        elif p25 < score <= p50:
            range_26_50.append((name, score))
        elif p50 < score <= p75:
            range_51_75.append((name, score))
        elif score > p75:
            range_76_100.append((name, score))

    # Display the results
    print("0% - 25% range:", range_0_25)
    print("26% - 50% range:", range_26_50)
    print("51% - 75% range:", range_51_75)
    print("76% - 100% range:", range_76_100)










def main():
    # Initialize an empty list to store edges
    edges = []


    # Read the CSV file
    with open('', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            edges.append(tuple(row))


    # Create a graph from the list of edges
    g = ig.Graph.TupleList(edges, directed=True)



