# Step Zero: Setup HTTP information to connect to GitHub API
# REQUIRES: http://docs.python-requests.org/en/master/user/install/
import requests

# Step One: Login to the user account through the "Basic Authentication" method.
user_name = input("Enter your GitHub Username: ")
password = input("Enter your GitHub Password: ")
#authentication = requests.get("https://api.github.com/", {"userid":user_name, "password":password})
#print(authentication.json)
# Step Two: Create an OAuth Token using the Basic Authentication login and an API request.
# authorization = requests.post("https://api.github.com/authorizations", {"note":"GitUp Authentication Token"}, json=None)


# Step Three: Perform actions for a user through the API using their OAuth token.