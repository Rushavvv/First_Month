import mysql.connector

try: 
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='University'
    )
    if connection.is_connected():
            print("Database connection successful")
except mysql.connector.Error as err:
    print(f"Error: {err}")


cursor = connection.cursor()

li = cursor.execute("SELECT * FROM Student")

results = cursor.fetchall()
li = [] 
for row in results: 
    li.append(row)
    print(row)

print(li)