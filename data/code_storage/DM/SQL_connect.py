import MySQLdb
import sys
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
#curs.execute(f"drop table 重平 ")

curs.execute(f"create table 重平 (id int, time varchar(20), spaces int)")
curs.execute(f"insert into 重平 values(1, '2019-01-01', 25)")
curs.execute(f"insert into 重平 values(2, '2019-01-02', 30)")


curs.execute(f"select * from 重平")
result = curs.fetchall()
print(result)

curs.close()
db.commit()
db.close()

