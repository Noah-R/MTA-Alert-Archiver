import pymysql
import alertfetcher

server = "scratching-post.cc0rktzgr4u0.us-east-1.rds.amazonaws.com"
database = "mydb"
username = "admin"
password = str(open("dbpw.txt").read())

df = alertfetcher.fetch('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts', writecsv=True)

conn = pymysql.connect(host=server, user=username, passwd=password, db=database, connect_timeout=5)

cur = conn.cursor()
for index, row in df.iterrows():
     sql = "INSERT INTO Alerts (time, start, end, route, header, description) values(%s, %s, %s, %s,%s, %s)"
     cur.execute(sql, (row.time, row.start, row.end, row.route, row.header, row.description))
conn.commit()