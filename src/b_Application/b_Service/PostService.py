from datetime import datetime
from src.e_Infra.SQLAlchemyBuilder import *
from src.e_Infra.BuildFlaskResponse import *


# Function that creates a new post #
def post_create_post(request_body):
    # Validating if user_id was given and if user exists #
    if request_body.get('user_id') is not None:
        select_user_query = f"select count(*) from strider.user where id_user = '{request_body['user_id']}'"
        try:
            select_user_query_result = sqlalchemy_execute_read_raw_query(select_user_query)
            if int(select_user_query_result[0][0]) < 1:
                return build_flask_response(404, {'Error Message': "User does not exist"})
        except Exception as e:
            return build_flask_response(400, {'Error Message': e})
    else:
        return build_flask_response(400, {'Error Message': 'Please provide user_id'})

    # Validating if post was given on body and if its size matches max length #
    if request_body.get('post') is None or len(request_body['post']) > 777 or len(request_body['post']) == 0:
        return build_flask_response(400, {'Error Message': 'Invalid post size'})

    # Validating if user is able to post today #
    to_day_post_count_query = f"select (select count(*) from strider.repost where user_id = '{request_body['user_id']}' and DATE(date_time) = CURDATE()) +  (select count(*) from strider.post where user_id = '{request_body['user_id']}' and DATE(date_time) = CURDATE())  as count"
    try:
        to_day_post_count_query_result = sqlalchemy_execute_read_raw_query(to_day_post_count_query)
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})
    try:
        if int(to_day_post_count_query_result[0][0]) >= 5:
            return build_flask_response(400, {'Error Message': "You have exceeded your daily post limit"})
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})

    # Executing insert #
    query = f"insert into strider.post (id_post, post, user_id, date_time) values ('{request_body['id_post']}', '{request_body['post']}', '{request_body['user_id']}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}');"
    try:
        sqlalchemy_execute_write_raw_query(query)
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})
    return build_flask_response(200, {'Message': 'Query successfully persisted'})


# Function that retrieves all posts from a given user #
def get_post_list(user_id, request_args_dict):
    # Validating page parameter #
    try:
        if request_args_dict.get('page') is None:
            page = 0
        else:
            page = int(request_args_dict.get('page'))
    except Exception as e:
        return build_flask_response(400, {'Error Message': f'Invalid page parameter - {e}'})

    # Retrieving post list #
    limit_start = 0 + (page * 5)
    limit_end = 5 + (page * 5)
    query = f"select * from strider.post where user_id = '{user_id}' order by date_time desc limit {limit_start},{limit_end};"
    try:
        query_result = sqlalchemy_execute_read_raw_query(query)
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})

    # Building response #
    result = []
    try:
        for item in query_result:
            result_dict = {}
            result_dict['id_post'] = item[0]
            result_dict['post'] = item[1]
            result_dict['user_id'] = item[2]
            result_dict['date_time'] = item[3]
            result.append(result_dict)
    except Exception as e:
        return build_flask_response(400, f'Result cast exception, please check your query {str(e)}')

    return build_flask_response(200, result)


# Retrieve all posts #
def get_all_posts_list(own_user_id, request_args_dict):
    # Validating page parameter #
    try:
        if request_args_dict.get('page') is None:
            page = 0
        else:
            page = int(request_args_dict.get('page'))
    except Exception as e:
        return build_flask_response(400, {'Error Message': f'Invalid page parameter - {e}'})

    # Validating following parameter #
    try:
        if request_args_dict.get('following') is not None:
            following = eval(request_args_dict.get('following').lower().capitalize())
        else:
            following = False
    except Exception as e:
        return build_flask_response(400, {'Error Message': f'Invalid following parameter - {e}'})

    # Retrieving post list #
    limit_start = 0 + (page * 10)
    limit_end = 10 + (page * 10)
    if following:
        query = f"select * from strider.post p where p.user_id in (select follows_user_id from strider.user_follows_user ufu where ufu.user_id = '{own_user_id}') order by date_time desc limit 0,10"
    else:
        query = f"select * from strider.post  order by date_time desc limit {limit_start},{limit_end};"
    try:
        query_result = sqlalchemy_execute_read_raw_query(query)
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})

    # Building response #
    result = []
    try:
        for item in query_result:
            result_dict = {}
            result_dict['id_post'] = item[0]
            result_dict['post'] = item[1]
            result_dict['user_id'] = item[2]
            result_dict['date_time'] = item[3]
            result.append(result_dict)
    except Exception as e:
        return build_flask_response(400, f'Result cast exception, please check your query {str(e)}')

    return build_flask_response(200, result)


# Function that reposts an existing post #
def post_repost(id_post, user_id, request_body, request_args_dict):
    # Validating post exists #
    select_post_query = f"select count(*) from strider.post where id_post = '{id_post}';"
    try:
        find_post_query_result = sqlalchemy_execute_read_raw_query(select_post_query)
        if int(find_post_query_result[0][0]) < 1:
            return build_flask_response(404, {'Error Message': "Post does not exist"})
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})

    # Validating user exists #
    select_user_query = f"select count(*) from strider.user where id_user = '{user_id}'"
    try:
        select_user_query_result = sqlalchemy_execute_read_raw_query(select_user_query)
        if int(select_user_query_result[0][0]) < 1:
            return build_flask_response(404, {'Error Message': "User does not exist"})
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})

    # Validating user can repost #
    to_day_post_count_query = f"select (select count(*) from strider.repost where user_id = '{user_id}' and DATE(date_time) = CURDATE()) +  (select count(*) from strider.post where user_id = '{user_id}' and DATE(date_time) = CURDATE())  as count"
    try:
        to_day_post_count_query_result = sqlalchemy_execute_read_raw_query(to_day_post_count_query)
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})
    try:
        if int(to_day_post_count_query_result[0][0]) >= 5:
            return build_flask_response(400, {'Error Message': "You have exceeded your daily post limit"})
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})

    # Validating quote #
    quote_str = str()
    try:
        if request_args_dict.get('quote') is not None:
            quote_str = request_args_dict['quote']
            if len(quote_str) > 777:
                return build_flask_response(400, {'Error Message': 'Quote exceeds max size'})
    except Exception as e:
        return build_flask_response(400, {'Error Message': f'Invalid quote parameter - {e}'})

    # Reposting a post #
    try:
        repost_final_query = f"insert into strider.repost(id_repost, post_id, user_id, quote, date_time)VALUES('{request_body['id_repost']}', '{id_post}', '{user_id}', '{quote_str}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}');"
        sqlalchemy_execute_write_raw_query(repost_final_query)
    except Exception as e:
        return build_flask_response(400, {'Error Message': e})
    return build_flask_response(200, {'Message': 'Query successfully persisted'})
