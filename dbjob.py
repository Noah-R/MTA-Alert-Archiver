import pymysql
import alertfetcher

def archive(event, context):
     server = "scratching-post.cc0rktzgr4u0.us-east-1.rds.amazonaws.com"
     database = "mydb"
     username = "admin"
     password = str(open("dbpw.txt").read())

     df = alertfetcher.fetch('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts')

     conn = pymysql.connect(host=server, user=username, passwd=password, db=database, connect_timeout=5)

     cur = conn.cursor()
     for item in df:#this can be future-proofed by converting item.keys() and item.values() into tuples rather than hard-coding
          sql = "INSERT INTO Alerts (time, start, end, route, header, description) values(%s, %s, %s, %s, %s, %s)"
          cur.execute(sql, (item['time'], item['start'], item['end'], item['route'], item['header'], item['description']))
     conn.commit()

#archive({}, {})