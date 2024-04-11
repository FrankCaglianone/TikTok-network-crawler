


## Usage 🛠️   

## Contributions 👥    [People that contributed to this project]

## License 📄
[MIT License](LICENSE)









# TikTok-network-crawler (Bachelor Research Project) ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
A Social Network Crawler in Python that, given a user or a list of users, fetches the user’s followings from the TikTok API and then recursively fetches the followings of those accounts. This creates a representation of the TikTok network to then compare it with other known social networks like Instagram and Meta.

## Project Purpose 🎯
This project is structured for those interested in network science, social media analysis, and data science enthusiasts. The 2 main purposes of this project are:
- Social Network Analysis: The purpose of this program is to create a representation of the TikTok network to study its structure and compare it with other known social networks like Instagram and Meta.
- Marketing and Research: Marketers and researchers could also use this code to identify trends and potential market niches within TikTok's ecosystem.

## Important Features ✨
- REST APIs: Utilizes POST requests to TikTok's API to gather data on user connections.




## Outputs 📦
The program saves the fetched data in 5 CSV files for subsequent analysis.
- parsing_list.csv: Maps usernames to integers reflecting the result of their data request
  - 1 = Parsed
  - 2 = Status code 403 User cannot be accessed
  - 3 = Statsus code 500 User not existent or found
  - 4 = Unknown
- queue.csv: Lists usernames fetched but not yet parsed, allowing for process resumption.
- saved_jsons.csv: Stores JSON responses from each user query.
- time_stamps.csv: Records timestamps for each response, noting multiple entries for users with numerous followees.
- network.csv: Contains tuples of "source" (username) and "destination" (their followee), foundational for network representation.



## Requirements 📋
- This software uses the TikTok Research API for which an account is needed, once the account is created a key and a secret will be provided which is mandatory to use the program, for more information on how to create an account please check [TikTok for Developers](https://developers.tiktok.com/)

- This software uses the "requests" package to send the POST requests to the TikTok API, so please make sure to have it installed otherwise it can be installed via pip with the following command:
  ```bash
  pip install requests
  ```
  Please note that this package requires Python >= 3.7.  For more information please check [requests](https://pypi.org/project/requests/)


## Project Structure 🏗️ 
The project is structured on 3 files:
1. main: The script is the entry point for the project. It uses argparse for command-line interaction, allowing users to input their API key, secret, and a starting username or a path to a CSV file containing a list of usernames. It automatically differentiates between a single username and a list of usernames based on the file extension, and delegates the parsed input to the appropriate functions in user_following_query.py based on the type of input provided.
   
2. create_access_token: Fundamental for handling authentication with the TikTok API. The script uses client credentials (a key and a secret) to obtain an access token from TikTok's OAuth endpoint. This token is essential for making authorized requests to the API.

3. user_following_query: This script is the one that parses the network. It executes POST requests to fetch the list of followees for given TikTok usernames, using the access tokens obtained by create_access_token.py, while saving the fetched data in the various CSV files for subsequent analysis. Implements robust error handling and logging mechanisms to manage and diagnose issues during the data fetching and parsing processes.













