import requests
import json

username = 'erfolgsarmee'
#user_id = 516679301

def get_user_information_by_username(username):
    user_info = {}
    url = 'https://www.instagram.com/{}/?__a=1'
    resp = requests.get(url=url.format(username)).json()
    userdata = resp["graphql"]["user"]
    user_info["id"] = userdata["id"]
    user_info["followers"] = userdata["edge_followed_by"]["count"]
    user_info["following"] = userdata["edge_follow"]["count"]
    user_info["profile_pic_url"] = userdata["profile_pic_url"]
    return user_info

def get_user_by_id(user_id):
    user = {}
    if user_id:
        base_url = "https://i.instagram.com/api/v1/users/{}/info/"
        #valid user-agent
        headers = {
            'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
        }
        try:
            res       = requests.get(base_url.format(user_id),headers=headers)
            user_info = res.json()
            user      = user_info.get('user',{})["username"]
        except Exception as e:
            print("getting user failed, due to '{}'".format(e.message))
    return user

print(get_user_information_by_username(username)["id"])
#print(get_user_by_id(user_id))