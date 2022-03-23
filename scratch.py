import requests
import gtfs_realtime_pb2
import time
import pandas as pd

url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fall-alerts' #all alerts
#url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts' #subway
#url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fmnr-alerts' #mnr
r = requests.get(url, headers={'x-api-key': 'q0l67K75Ja59qvzUcrvJR6wqufloVMew3UlCcRuk'})

feed=gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(r.content)

results = {}
count=0

for entity in feed.entity:
    if entity.HasField('alert'):
        if(len(entity.alert.active_period)==0 or not entity.alert.active_period[0].HasField('start') or entity.alert.active_period[0].start<time.time()):#if the time is blank, or the start time is blank, or the start time is in the past
            informed = ""
            header = ""
            description = ""
            for informed in (entity.alert.informed_entity):
                informed = "Informed: \n"+str(informed)+"\n"
            if(len(entity.alert.header_text.translation)>0):
                header = entity.alert.header_text.translation[0].text+"\n"
            if(len(entity.alert.description_text.translation)>0):
                description = entity.alert.description_text.translation[0].text+"\n"
            results[count]=[informed, header, description]
            count+=1
df = pd.DataFrame.from_dict(results, orient="index", columns=["informed", "header", "description"])
df.to_csv("results.csv")