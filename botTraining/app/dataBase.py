import psycopg2

cursor = None
connection = None


def print_db(query):
    try:
        connection = psycopg2.connect(
            dbname="My_db_for_bot",
            user="postgres",
            password="Qazwsxedc_0904",
            host="localhost",
            port=5434
        )

        cursor = connection.cursor()

        cursor.execute(query)

        records = cursor.fetchall()

        return records

    except Exception as error:
        print("Ошибка при работе с PostgreSQL:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Соединение с базой данных закрыто.")


def execute_db(query):
    connection = psycopg2.connect(
        dbname="My_db_for_bot",
        user="postgres",
        password="Qazwsxedc_0904",
        host="localhost",
        port=5434
    )

    cursor = connection.cursor()

    cursor.execute(query)

    connection.commit()
