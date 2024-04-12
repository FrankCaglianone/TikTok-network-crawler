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
This software uses the TikTok Research API for which an account is needed, once the account is created a key and a secret will be provided, those are mandatory to use the program, for more information on how to create an account please check [TikTok for Developers](https://developers.tiktok.com/)

This software uses the "requests" package to send the POST requests to the TikTok API, so please make sure to have it installed otherwise it can be installed via pip with the following command:
  ```bash
  pip install requests
  ```
  Please note that this package requires Python >= 3.7.  For more information please check [requests](https://pypi.org/project/requests/)

## Usage 🛠️
To execute the program, a default job submission script, submit_job.sh, is available. This script is designed to submit jobs to the Slurm workload manager on remote servers using the sbatch command. 

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

main: The script acts as the project's entry point, utilizing argparse for command-line options to accept an API key, secret, and either a single username or a path to a CSV file of usernames. It can automatically distinguish between a single username and multiple ones from a file, routing the input to corresponding functions in user_following_query.py.
   
create_access_token: This script manages authentication with the TikTok API by using client credentials (a key and a secret) to obtain an access token from TikTok's OAuth endpoint. If authentication fails, it exits immediately to alert the user. The script also supports concurrent programming for token generation to cope with their 2-hour expiration.

user_following_query: This script handles the network parsing, sending POST requests to retrieve followees for specified TikTok usernames. It uses tokens from create_access_token.py and stores results in CSV files for subsequent analysis. It features robust error handling and logging to troubleshoot data fetching and parsing issues.



## Contributions 👥 
A special thanks to Prof. Luca Maria Aiello (Associate Professor at ITU Copenhagen) for helping me and supervising me throughout this project. [lajello](https://www.lajello.com/)


## License 📄
[MIT License](LICENSE)










