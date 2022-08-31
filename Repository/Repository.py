import sqlite3


def getConnectionString():
    return sqlite3.connect('Repository/ApplicationDb.db')


connectionString = None


def createUserTable():
    try:
        global connectionString
        connectionString = getConnectionString()
        cursor = connectionString.cursor()

        create_table = "CREATE TABLE IF NOT EXISTS Users (id int, username text, password text)"

        result = cursor.execute(create_table)

        if result.rowcount > 0:
            print("Table Successfully Created")

    except sqlite3.OperationalError:
        raise sqlite3.OperationalError

    finally:
        connectionString.commit()
        connectionString.close()


def createItemTable():
    try:
        global connectionString
        connectionString = getConnectionString()
        cursor = connectionString.cursor()

        create_table = "CREATE TABLE IF NOT EXISTS Items (id INTEGER PRIMARY KEY, name text, price long)"

        result = cursor.execute(create_table)
        print(result.rowcount)
        if result.rowcount > 0:
            print("Table Successfully Created")

    except sqlite3.OperationalError:
        raise sqlite3.OperationalError

    finally:
        connectionString.commit()
        connectionString.close()


if __name__ == "__main__":
    pass
