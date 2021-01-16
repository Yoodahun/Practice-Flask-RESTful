import sqlite3

#initialize connection

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

#create table
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'jose', 'asdf')

#insert data
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

#insert multiple data
users = [
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'xyz')

]

cursor.executemany(insert_query,users)

#select query
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()