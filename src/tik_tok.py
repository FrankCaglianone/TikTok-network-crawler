import requests



header = {
    "Authorization": "Bearer your_access_token",
    "Content-Type": "application/json"
}

dat = {
    "username": "francescocaglianone",  
    "max_count": 10,  # Optional: Adjust the number of results as needed
}

response = requests.post("https://open.tiktokapis.com/v2/research/user/followers/", headers=header, json=dat)


if response.status_code == 200:
    followers = response.json()
    print(followers)
else:
    print("Failed to retrieve followers. Status code:", response.status_code)
