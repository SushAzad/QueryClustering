import pymysql
import configparser

# print cursor function
def pc(cursor):
	for x in cursor:
		print(x)

# reads the config file
config = configparser.ConfigParser()
config.read("config.ini")

conn = pymysql.connect(
	host = config.get("Database", "mysql_ip"),
	user = config.get("Database", "mysql_user"),
	passwd = config.get("Database", "mysql_pw"))

mycursor = conn.cursor()

mycursor.execute("SHOW DATABASES")

pc(mycursor)

# conn.commit()