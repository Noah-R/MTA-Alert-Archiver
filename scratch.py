import requests
import gtfs_realtime_pb2
import time
import datetime
import pandas as pd

#url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fall-alerts' #all alerts
url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts' #subway
#url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fmnr-alerts' #mnr
r = requests.get(url, headers={'x-api-key': open("key.txt").read()})

feed=gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(r.content)

results = {}
count=0

for entity in feed.entity:
    if entity.HasField('alert'):
        for t in entity.alert.active_period:
            if(t.start<=time.time() and t.end>=time.time()):
                start = ""
                end = ""
                route = []
                station = []
                header = ""
                description = ""
                
                start = datetime.datetime.fromtimestamp(t.start).strftime('%Y-%m-%d %H:%M:%S')
                end = datetime.datetime.fromtimestamp(t.end).strftime('%Y-%m-%d %H:%M:%S')

                for inf in entity.alert.informed_entity:
                    if(inf.HasField('route_id')):
                        route.append(inf.route_id)
                    if(inf.HasField('stop_id')):
                        station.append(inf.stop_id)
                route = str(route)[1:-1]
                station = str(station)[1:-1]

                if(len(entity.alert.header_text.translation)>0):
                    header = entity.alert.header_text.translation[0].text
                if(len(entity.alert.description_text.translation)>0):
                    description = entity.alert.description_text.translation[0].text

                results[count]=[start, end, route, station, header, description]
                count+=1
                break

df = pd.DataFrame.from_dict(results, orient="index", columns=["start_time", "end_time", "route", "station", "header", "description"])
df.to_csv("results.csv")