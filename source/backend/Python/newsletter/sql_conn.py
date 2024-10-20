import mysql.connector

def innit_conn(query, host='127.0.0.1', user='root', password='M12n2B3v4!', database='uohackathon2024'):

    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
    if not db.is_connected():
        raise ConnectionError(f'Python is unable to make a local connection to database {database}:{host}')

    cursor = db.cursor()

    cursor.execute(query)

    result = cursor.fetchall()
    return result