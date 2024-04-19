import requests

# import create_access_token


def get_top_videos(user_id, access_token):
    url = 'https://open.tiktokapis.com/v2/research/video/query/?fields=id,video_description,create_time'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    body = {
        "query": {
            "and": [
                {
                    "operation": "IN",
                    "field_name": "region_code",
                    "field_values": ["JP", "US"]
                },
                {
                    "operation":"EQ",
                    "field_name":"hashtag_name",
                    "field_values":["animal"]
                }
            ],
            "not": [
                {
                    "operation": "EQ",
                    "field_name": "video_length",
                    "field_values": ["SHORT"]
                }
            ]
        },
        "max_count": 10,
        "cursor": 0,
        "start_date": "20230101",
        "end_date": "20230115"  
    }
    
    response = requests.post(url=url, headers=headers, json=body)
    
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text





access_token = ""
user_id = 'francescocaglianone'
top_videos = get_top_videos(user_id, access_token)

print(top_videos)
