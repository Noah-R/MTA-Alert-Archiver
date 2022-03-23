import requests
import gtfs_realtime_pb2
import time
import datetime
import pandas as pd

#url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fall-alerts' #all alerts
url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts' #subway
#url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fmnr-alerts' #mnr
r = requests.get(url, headers={'x-api-key': 'q0l67K75Ja59qvzUcrvJR6wqufloVMew3UlCcRuk'})

feed=gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(r.content)

results = {}
count=0

for entity in feed.entity:
    if entity.HasField('alert'):
        if(len(entity.alert.active_period)==0 or not entity.alert.active_period[0].HasField('start') or entity.alert.active_period[0].start<time.time()):#if the time is blank, or the start time is blank, or the start time is in the past
            start = ""
            informed = ""
            header = ""
            description = ""
            
            if(len(entity.alert.active_period)>0 and entity.alert.active_period[0].HasField('start')):
                start = datetime.datetime.fromtimestamp(entity.alert.active_period[0].start).strftime('%Y-%m-%d %H:%M:%S')

            for inf in entity.alert.informed_entity:
                if(inf.HasField('route_id')):
                    informed += "Route: "+inf.route_id+" "

                if(inf.HasField('stop_id')):
                    informed = "Stop: "+inf.stop_id+" "

            if(len(entity.alert.header_text.translation)>0):
                header = entity.alert.header_text.translation[0].text

            if(len(entity.alert.description_text.translation)>0):
                description = entity.alert.description_text.translation[0].text

            results[count]=[start, informed, header, description]
            count+=1

df = pd.DataFrame.from_dict(results, orient="index", columns=["start", "informed", "header", "description"])
df.to_csv("results.csv")