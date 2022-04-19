from datetime import datetime
from src.e_Infra.SQLAlchemyBuilder import *
from src.e_Infra.BuildFlaskResponse import *
from src.e_Infra.RegexValidator import validate_username


# Function that retrieves all users #
def get_user_list():
    query = f"select id_user, username, date_joined from strider.user"
    try:
        query_result = sqlalchemy_execute_read_raw_query(query)
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})

    result = []
    try:
        for item in query_result:
            result_dict = {}
            result_dict['id_user'] = item[0]
            result_dict['username'] = item[1]
            result_dict['date_joined'] = item[2].strftime("%B %d, %Y")
            result.append(result_dict)
    except Exception as e:
        return build_flask_response(400, f'Result cast exception, please check your query {str(e)}')

    return build_flask_response(200, result)


# Function that a given user by the id #
def get_user_by_id(user_id):
    query = f"select id_user, username, date_joined from strider.user where id_user = '{user_id}'"
    try:
        query_result = sqlalchemy_execute_read_raw_query(query)
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})

    result = []
    try:
        for item in query_result:
            result_dict = {}
            result_dict['id_user'] = item[0]
            result_dict['username'] = item[1]
            result_dict['date_joined'] = item[2]
            result.append(result_dict)
    except Exception as e:
        return build_flask_response(400, f'Result cast exception, please check your query {str(e)}')

    return build_flask_response(200, result)


# Function that sets a user to follow another user #
def post_user_follow(user_id, user_followed_id):
    # Validates if both given ids are the same #
    if user_id == user_followed_id:
        return build_flask_response(400, {'Error Message': "User can't follow himself"})

    query = f"insert into strider.user_follows_user(user_id, follows_user_id) values ('{user_id}', '{user_followed_id}');"
    try:
        sqlalchemy_execute_write_raw_query(query)
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})
    return build_flask_response(200, {'Message': 'Query successfully persisted'})


# Function that sets a user to unfollow another user #
def post_user_unfollow(user_id, user_followed_id):
    # Validates if both given ids are the same #
    if user_id == user_followed_id:
        return build_flask_response(400, {'Error Message': "User can't unfollow himself"})

    query = f"delete from strider.user_follows_user where user_id = '{user_id}' AND follows_user_id = '{user_followed_id}';"
    try:
        sqlalchemy_execute_write_raw_query(query)
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})
    return build_flask_response(200, {'Message': 'Query successfully persisted'})


# Function that retrieves a list of user followers #
def get_user_followers(user_id):
    query = f"select user_id from strider.user_follows_user where follows_user_id = '{user_id}'"
    try:
        query_result = sqlalchemy_execute_read_raw_query(query)
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})

    result = []
    try:
        for item in query_result:
            result_dict = {}
            result_dict['user_id'] = item[0]
            result.append(result_dict)
    except Exception as e:
        return build_flask_response(400, f'Result cast exception, please check your query {str(e)}')

    return build_flask_response(200, result)


# Function that retrieves a list of user that are following the given user #
def get_user_following(user_id):
    query = f"select follows_user_id from user_follows_user where user_id = '{user_id}'"
    try:
        query_result = sqlalchemy_execute_read_raw_query(query)
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})

    result = []
    try:
        for item in query_result:
            result_dict = {}
            result_dict['follows_user_id'] = item[0]
            result.append(result_dict)
    except Exception as e:
        return build_flask_response(400, f'Result cast exception, please check your query {str(e)}')

    return build_flask_response(200, result)


# Function that creates a new user #
def create_user(request_body):
    # Validates if user_name matches regex pattern #
    valid_user_name = validate_username(request_body['username'])
    if not valid_user_name:
        return build_flask_response(400, {'Error Message': 'Invalid user_name'})

    query = f"INSERT INTO strider.user (id_user, username, date_joined) VALUES ('{request_body['id_user']}', '{request_body['username']}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}');"
    try:
        sqlalchemy_execute_write_raw_query(query)
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})
    return build_flask_response(200, {'Message': 'Query successfully persisted'})
