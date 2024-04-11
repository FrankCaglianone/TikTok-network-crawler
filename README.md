# TikTok-network-crawler (Bachelor Research Project) ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
This project explores the dynamics of social networks by mapping the connections within TikTok's ecosystem. Starting from a single username or a list of usernames provided in a CSV file, the program employs a series of POST requests to a TikTok API to fetch the user’s followings and then recursively fetches the followings of those accounts. This creates a representation of the TikTok network for comparative network analysis with other social platforms like Instagram and Meta.


## Project Purpose 🎯
This project is structured for those interested in network science, social media analysis, and data science enthusiasts. The 2 main purposes of this project are:
- Social Network Analysis: The purpose of this program is to create a representation of the TikTok network to study its structure and compare it with other known social networks like Instagram and Meta.
- Marketing and Research: Marketers and researchers could also use this code to identify trends and potential market niches within TikTok's ecosystem.

## Important Features ✨
- REST APIs: Utilizes POST requests to TikTok's API to gather data on user connections.
- Concurrent Programming: For efficiency and speed.
- OS Signaling: To ensure that data is saved upon succesfull or unsucesfull completion.


## Outputs 📦
The program saves the fetched data in 5 CSV files for subsequent analysis in 'src/outputs'. Please note that if the file do not exist they will be created, if they exist they will get overwritten.
- parsing_list.csv: Maps usernames to integers reflecting the result of their data request
  - 1 = Parsed
  - 2 = Status code 403 User cannot be accessed
  - 3 = Statsus code 500 User not existent or found
  - 4 = Unknown
- queue.csv: Lists usernames fetched but not yet parsed, allowing for process resumption.
- saved_jsons.csv: Stores JSON responses from each user query.
- time_stamps.csv: Records timestamps for each response, noting multiple entries for users with numerous followees.
- network.csv: Contains tuples of "source" (username) and "destination" (their followee), fundamental for network representation.



## Requirements 📋
This software uses the TikTok Research API for which an account is needed, once the account is created a key and a secret will be provided which is mandatory to use the program, for more information on how to create an account please check [TikTok for Developers](https://developers.tiktok.com/)

This software uses the "requests" package to send the POST requests to the TikTok API, so please make sure to have it installed otherwise it can be installed via pip with the following command:
  ```bash
  pip install requests
  ```
  Please note that this package requires Python >= 3.7.  For more information please check [requests](https://pypi.org/project/requests/)

## Usage 🛠️
To execute the program, a default job submission script, submit_job.sh, is available. This script is designed to submit jobs through a sbatch workload manager on remote servers. 

Alternatively, the program can be run locally on your device using the command:
```bash
  python3 src/main.py key secret user_input
```
Please note, running the program locally is discouraged as it is resource-intensive.

Please remember in both cases to substitute:
- key: API key for authentication.
- secret: API secret for authentication.
- user_input: Path to the usernames input or a single username. Ends with .csv for list input.

  
## Project Structure 🏗️ 
The project is structured on 3 files:

main: The script is the entry point for the project. It uses argparse for command-line interaction, allowing users to input their API key, secret, and a starting username or a path to a CSV file containing a list of usernames. It automatically differentiates between a single username and a list of usernames based on the file extension, and delegates the parsed input to the appropriate functions in user_following_query.py based on the type of input provided.
   
create_access_token: Fundamental for handling authentication with the TikTok API. The script uses client credentials (a key and a secret) to obtain an access token from TikTok's OAuth endpoint. This token is essential for making authorized requests to the API. It exits the program if authentication fails due to incorrect credentials or other issues, ensuring that the user is immediately aware of authentication problems. Concurrent programming was used to create multiple access tokens since they expire after 2 hours.

user_following_query: This script is the one that parses the network. It executes POST requests to fetch the list of followees for given TikTok usernames, using the access tokens obtained by create_access_token.py, while saving the fetched data in the various CSV files for subsequent analysis. Implements robust error handling and logging mechanisms to manage and diagnose issues during the data fetching and parsing processes.





## Contributions 👥 



## License 📄
[MIT License](LICENSE)










