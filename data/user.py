import json

# Load user data from JSON file
def load_users():
    with open('data/user_data.json', 'r') as file:
        return json.load(file)['users']

# Save user data to JSON file
def save_users(users):
    with open('data/user_data.json', 'w') as file:
        json.dump({"users": users}, file, indent=4)

# Create a new user
def create_user(user_name, user_password, favorite_genres):
    users = load_users()
    user_id = len(users) + 1  
    new_user = {
        "user_id": user_id,
        "user_name": user_name,
        "user_password": user_password,
        "user_info": sorted(favorite_genres)  # Sort favorite genres
    }
    users.append(new_user)
    save_users(users)

# Update an existing user
def update_user(user_id, user_name=None, user_password=None, favorite_genres=None):
    users = load_users()
    for user in users:
        if user['user_id'] == user_id:
            if user_name is not None:
                user['user_name'] = user_name
            if user_password is not None:
                user['user_password'] = user_password
            if favorite_genres is not None:
                user['user_info'] = sorted(favorite_genres)  # Sort favorite genres
            break
    save_users(users)