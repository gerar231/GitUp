# Step Zero: Setup HTTP information to connect to GitHub API
# REQUIRES: http://docs.python-requests.org/en/master/user/install/
import requests
import json

# Step One: Login to the user account through the "Basic Authentication" method.
user_name = input("Enter your GitHub Username: ")
password = input("Enter your GitHub Password: ")

# Step Two: Create an OAuth Token using the Basic Authentication login and an API request.
# TO-DO: add in check for a token that has the GitUp fingerprint
note = "GitUp Authentication Token v1.0"
note_url = "https://github.com/gerar231/GitUp"
authentication = requests.post("https://api.github.com/authorizations", json={"note":note, "note_url":note_url, "fingerprint":str("GitUp"+user_name)}, auth=(user_name, password))
print(authentication.json())
user_token = authentication.json()['token']


# Step Three: Perform actions for a user through the API using their OAuth token.
# example, get the number of user private repositories using their user token (not login)
user_info = requests.get("https://api.github.com/user", params={"access_token":user_token})
print(user_info.json())