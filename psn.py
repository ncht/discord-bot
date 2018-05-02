import sys
sys.path.append("./third_party/psn-api")

from src.Auth import Auth
from src.User import User
from src.Friend import Friend
from setting import setting

authenticated_friends = setting["auth_friends"]

owner = setting["psn_owner"]

token_pair = None

tokens = {
    "npsso": setting["npsso"]
}

user = None
friend = None

def initialize():
    global token_pair
    global tokens
    global user
    global friend

    token_pair = Auth.GrabNewTokens(setting["grab_token"])
    if token_pair == None:
        return False

    tokens["oauth"] = token_pair[0]
    tokens["refresh"] = token_pair[1]
    user = User(tokens)
    friend = Friend(tokens)

    return True

def get_user_playing():
    user_data = user.me()

    if "profile" not in user_data \
         or "presences" not in user_data["profile"] \
         or len(user_data['profile']['presences']) <= 0 \
         or "titleName" not in user_data['profile']['presences'][0]:
        return ""

    return user_data['profile']['presences'][0]['titleName']

def get_user_state(psn_id):
    user_data = None
    if psn_id == owner:
        user_data = user.me()
    elif psn_id in authenticated_friends.keys():
        user_data = friend.get_info(authenticated_friends[psn_id])
    else:
        return None

    if "profile" not in user_data \
        or "presences" not in user_data["profile"] \
        or len(user_data['profile']['presences']) <= 0:
        return None

    return user_data['profile']['presences'][0]
