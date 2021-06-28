import mysql.connector as mysql
user_name = "root"
password = "mysql"
host = "test"  # docker-composeで定義したMySQLのサービス名
database_name = "mysql"


conn = mysql.connect(
    host="test",
    user="root",
    passwd="mysql",
    port=3306,
    database="mysql"
)

conn.ping(reconnect=True)

print(conn.is_connected())