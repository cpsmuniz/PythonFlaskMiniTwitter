# Flask Imports #
from src.e_Infra.FlaskBuilder import *

from src.b_Application.b_Service.UserService import *


# Retrieve list of all users #
@app.route('/user', methods=['GET', 'POST'])
def user_list():
    # Routing request to /user GET method #
    if request.method == 'GET':
        result = get_user_list()
        return result
    # Routing request to /user POST method #
    if request.method == 'POST':
        result = create_user(request.json)
        return result


# Retrieve a specific user by its id #
@app.route('/user/<user_id>', methods=['GET'])
def user_by_id(user_id):
    result = get_user_by_id(user_id)
    return result


# Sets a given user to follow another given user #
@app.route('/user/<user_id>/follow/<user_followed_id>', methods=['POST'])
def user_follow(user_id, user_followed_id):
    result = post_user_follow(user_id, user_followed_id)
    return result


# Sets a given user to unfollow another given user #
@app.route('/user/<user_id>/unfollow/<user_followed_id>', methods=['DELETE'])
def user_unfollow(user_id, user_followed_id):
    result = post_user_unfollow(user_id, user_followed_id)
    return result


# Retrieves a list of followers of a given user #
@app.route('/user/<user_id>/followers', methods=['GET'])
def user_followers(user_id):
    result = get_user_followers(user_id)
    return result


# Retrieves a list of users that a given user is following #
@app.route('/user/<user_id>/following', methods=['GET'])
def user_following(user_id):
    result = get_user_following(user_id)
    return result

