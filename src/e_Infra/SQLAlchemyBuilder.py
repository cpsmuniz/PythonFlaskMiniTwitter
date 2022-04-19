import os
import sqlalchemy


sqlalchemy_engine = None


def sqlalchemy_execute_read_raw_query(query):
    global sqlalchemy_engine
    if not sqlalchemy_engine:
        try:
            sqlalchemy_engine = sqlalchemy.create_engine(os.environ['mysql_connection_string'])
        except Exception as e:
            raise Exception(f'Engine creation failed - {e}')
    try:
        with sqlalchemy_engine.connect() as con:
            try:
                result = con.execute(query)
            except Exception as e:
                raise Exception(f'Invalid query - {e}')
            try:
                result_list = build_sqlalchemy_list_result(result)
            except Exception as e:
                raise Exception(f'Invalid building list - {e}')
            con.close()
    except Exception as e:
        raise Exception(f'Connection parameters invalid - {e}')
    return result_list


def sqlalchemy_execute_write_raw_query(query):
    global sqlalchemy_engine
    if not sqlalchemy_engine:
        try:
            sqlalchemy_engine = sqlalchemy.create_engine(os.environ['mysql_connection_string'])
        except Exception as e:
            raise Exception(f'Engine creation failed - {e}')
    try:
        con = sqlalchemy_engine.connect()
    except Exception as e:
        raise Exception(f'Connection parameters invalid - {e}')
    try:
        con.execute(query)
    except Exception as e:
        raise Exception(f'Invalid query - {e}')


def build_sqlalchemy_list_result(result):
    try:
        list_of_results = list()
        for row in result:
            final_item = list()
            for item in row:
                final_item.append(item)
            list_of_results.append(final_item)
    except Exception as e:
        raise Exception(e)
    return list_of_results

