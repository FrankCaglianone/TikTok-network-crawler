# TikTok-network-crawler (Bachelor Research Project) ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
This repository contains the source code for the bachelor research project titled "Using Algorithms to Identify Climate Activism Trends on TikTok." This research was conducted at the IT University of Copenhagen under the supervision of [Prof. Luca Maria Aiello](https://www.lajello.com/).
The research project explores the network dynamics of TikTok users engaged in climate activism, employing network science methodologies to map and analyze interactions and influence within this digital community.

#### This software is versatile and can be adapted to analyze the network dynamics of users engaged in various topics. By modifying the initial set of users input into the algorithm, researchers can repurpose the tool to explore different areas of interest.

<br>

## Project Purpose 🎯    [The purpose of the project, what can it be used for]
The goal of this project was to answer the following questions:
1. What topics and trends are commonly associated with climate activism?
2. Where are most climate activists located?
3. How can we get more people involved in climate activism?

<br>

## Important Features ✨
- Network Construction: Utilizes the TikTok Research API to construct a network starting from known climate activist users. The snowball sampling method was used, implemented with the Breadth-First Search technique to systematically expand the network.
- Influence Analysis: Applies PageRank to identify influential users within the network.
- Network Backboning: Uses the algorithm by Michele Coscia and Frank M. H. Neffke to filter out less significant interactions, focusing on key relationships using the Noise-Corrected method. [For more info](https://ieeexplore.ieee.org/abstract/document/7929996)
- Community Detection: Uses the Louvain algorithm to detect communities to further analyze predominant discussion topics.
- Hashtag Analysis: Analyzes hashtags to identify trending topics within different user influence levels and communities. It divides tha data in TF and TF-IDF.

<br>

## Tools & Technologies ⚙️
- TikTok Research API
- Requests Library
- Igraph
- Numpy
- Matplotlib
- Gephi (Yifan Hu Layout)
- Network Backboning Algorithm by Michele Coscia and Frank M. H. Neffke.

<br>

## Requirements 📋    



## Project Structure 🏗️
```bash
/TikTok-network-crawler
    ├── data/                  # Contains datasets used in analyses
    ├── scripts/
        ├── user_following_query.py  # Implements snowball sampling using BFS
        ├── network_analysis.py      # Performs network analysis including PageRank
    ├── results/
        ├── network.csv         # Edges representing the network structure
        ├── community_data.csv  # Results from community detection
    ├── figures/                # Visualization of networks and results
    ├── README.md
```




<br>
<br>

## Work In Progress 🚧


## Usage 🛠️   [Instructions and examples for using your project. This could include code snippets or command line examples.]

## Contributions 👥    [People that contributed to this project]

## License 📄
[MIT License](LICENSE)






