#!/usr/bin/python3

import requests
from requests.auth import HTTPBasicAuth
from config import userName, ghToken


API_ENDPOINT = "https://api.github.com/users/"
APPLICATION_JSON = "application/vnd.github.v3+json"

doReactToAction = True


class NotValidModeException(Exception):
    pass


def doFollow(user, mode):
    print(f"Doing {mode} for user {user}")

    action_endpoint = f"https://api.github.com/user/following/{user}"

    if mode.lower() == "put":
        requests.put(action_endpoint, headers={
                     "Accept": APPLICATION_JSON}, auth=HTTPBasicAuth(userName, ghToken))
    elif mode.lower() == "delete":
        requests.delete(action_endpoint, headers={
                        "Accept": APPLICATION_JSON}, auth=HTTPBasicAuth(userName, ghToken))
    else:
        raise NotValidModeException(f"'{mode} is not a valid mode")


def get(url):
    r = requests.get(url, headers={
                     "Accept": APPLICATION_JSON}, auth=HTTPBasicAuth(userName, ghToken))
    return r.json()


def ulist(data):
    return [user['login'] for user in data]


def newFollowers(followers, following):
    dif = []
    for user in followers:
        if user not in following:
            dif.append(user)
    return dif


def notFollowers(followers, following):
    dif = []
    for user in following:
        if user not in followers:
            dif.append(user)
    return dif


followers = ulist(get(API_ENDPOINT + userName + "/followers"))
following = ulist(get(API_ENDPOINT + userName + "/following"))

newFollowersList = newFollowers(followers, following)
notFollowersList = notFollowers(followers, following)

print("new followers: ", newFollowersList)
print("not followers: ", notFollowersList)


if doReactToAction:

    for user in notFollowersList:
        doFollow(user, "DELETE")

    for user in newFollowersList:
        doFollow(user, "PUT")
