import requests

# import create_access_token



# hashtag_names



def get_top_videos(username, access_token):
    url = 'https://open.tiktokapis.com/v2/research/video/query/?fields=id,username,view_count'   
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    body = {
        "query": {
            "and": [
                {
                    "operation": "EQ",
                    "field_name": "username",
                    "field_values": [username]
                },
            ],
        },
        "max_count": 10,
        "start_date": "20240417",
        "end_date": "20240419"  
    }
    
    response = requests.post(url=url, headers=headers, json=body)
    
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text





access_token = ""
user_id = "alessialanza"
top_videos = get_top_videos(user_id, access_token)

print(top_videos)
