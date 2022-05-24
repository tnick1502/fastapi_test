import sqlite3
conn = sqlite3.connect('database.sqlite3')
cur = conn.cursor()
#cur.execute("""INSERT INTO users(id, email, username, password_hash)
   #VALUES('00001', 'mail.ru', 'user1', 'password1');""")
#conn.commit()

cur.execute("SELECT * FROM users;")
one_result = cur.fetchone()
print(one_result)

#cur.execute("""INSERT INTO operations(id, user_id, date, kind, amount, description)
   #VALUES('00001', '00001', '17-19-2021', 'income', '10', 'test');""")
#conn.commit()
