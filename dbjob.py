import pyodbc
import alertfetcher

server = "scratching-post.cc0rktzgr4u0.us-east-1.rds.amazonaws.com"
database = "mydb"
username = "admin"
password = str(open("dbpw.txt").read())

df = alertfetcher.fetch('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts', writecsv=True)

cnxn = pyodbc.connect("DRIVER={SQL Server};SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password+"--enable-cleartext-plugin")#LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN=y
input("success!")
cursor = cnxn.cursor()
for index, row in df.iterrows():
     cursor.execute("INSERT INTO Alerts (time, start, end, route, header, description) values(?, ?, ?,?,?)", row.time, row.start, row.end, row.route, row.header, row.description)
cnxn.commit()
cursor.close()