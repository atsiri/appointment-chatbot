import psycopg2
from datetime import datetime, timedelta

# Define the database connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'booking',
    'user': 'postgres',
    'password': 'password'
}

connection = psycopg2.connect(
                host=db_params["host"],
                port=db_params["port"],
                database=db_params["database"],
                user=db_params["user"],
                password=db_params["password"]
                )

def DataSelect(name, date, start, end, updated_at):
    '''
    Pushes Descriptive Analytics Data to the Database
    '''
    cursor = connection.cursor()
    
    postgres_select_query = """SELECT * FROM appointment WHERE day_date = (%s) AND start_time = (%s);""".format(date, start)
    
    cursor.execute(postgres_select_query)
    
    connection.commit()
    return(postgres_select_query)

def DataInsert(name, date, start, end, updated_at):
    cursor = connection.cursor()
    
    postgres_insert_query = """INSERT INTO appointment(name, day_date, start_time, end_time, updated_at);""".format(name, date, start, end, datetime.now())
    
    cursor.execute(postgres_insert_query)
    
    connection.commit()
    print("Your appointment is set at", date, start)