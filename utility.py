import configuration as config
import pandas as pd

from mysql.connector import connect, Error

def get_query_result(query):
    try:
        with connect(host= config.HOST, user= config.USER, password= config.PASSWORD,  database=config.DATABASE) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
    except Error as e:
        print(e)
        return e

def insert_data(query, data):
    try:
        with connect(host= config.HOST, user= config.USER, password= config.PASSWORD) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                connection.commit()

    except Error as e:
        print(e)

def get_sql_result_df(query):
    try:
        with connect(host= config.HOST, user= config.USER, password= config.PASSWORD) as connection:
            result = pd.read_sql(query, connection)
            return result

    except Error as e:
        print(e)
