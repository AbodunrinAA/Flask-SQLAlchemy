import sqlite3

connectionString = sqlite3.connect('UserDb.db')

cursor = connectionString.cursor()

# create_table = "CREATE TABLE UserTable (id int, username text, password text)"

# cursor.execute(create_table)

# user = (100, 'Baba', 'Opeyemi')

# insert_query = "INSERT INTO UserTable VALUES (?, ?, ?)"

# cursor.execute(insert_query, user)
users = [
    (101, 'Tobi', 'Opeyemi'),
    (102, 'Bimpe', 'Opeyemi')
]

# cursor.executemany(insert_query, users)

select_query = "SELECT * FROM UserTable"

for u in cursor.execute(select_query):
    print(u)

connectionString.commit()

connectionString.close()
