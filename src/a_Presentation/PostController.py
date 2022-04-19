# Flask Imports #
from src.e_Infra.FlaskBuilder import *

# Service Imports #
from src.b_Application.b_Service.PostService import *


# Create a new post #
@app.route('/post', methods=['POST'])
def create_post():
    return post_create_post(request.json)


# Retrieve all posts from a given user #
@app.route('/post/user/<user_id>', methods=['GET'])
def get_post_list_by_user(user_id):
    return get_post_list(user_id, request.args.to_dict())


# Retrieve all posts #
@app.route('/post/<own_user_id>', methods=['GET'])
def get_all_user_posts_list(own_user_id):
    return get_all_posts_list(own_user_id, request.args.to_dict())


# Repost an existing post #
@app.route('/repost/<id_post>/user/<user_id>', methods=['POST'])
def create_repost(id_post, user_id):
    return post_repost(id_post, user_id, request.json, request.args.to_dict())

