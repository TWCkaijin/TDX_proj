import MySQLdb
# syntax table : https://qaz741012.github.io/2018/03/21/manipulate_MySQL_by_python3_with_mysqlclient_module/
# second table : https://www.796t.com/content/1548505830.html
db= MySQLdb.connect(
        host='webserverdatabase.cmstfznt40ot.ap-southeast-2.rds.amazonaws.com',
        port = 3306,
        user='AFD_Kai',
        passwd='AFD_Kai_PythonMaster',
        db ='GDSC',
        )
curs = db.cursor()



curs.execute("SELECT VERSION()")

data = curs.fetchall()

print(f"Database version : {data}")
db.closed()

