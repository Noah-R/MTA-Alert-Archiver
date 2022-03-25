import requests
import gtfs_realtime_pb2
import time
import datetime
import pandas as pd

def fetch(url, writecsv=False):
    r = requests.get(url, headers={'x-api-key': open("key.txt").read()})

    feed=gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(r.content)

    results = {}
    count=0

    for entity in feed.entity:
        if entity.HasField('alert'):
            for t in entity.alert.active_period:
                if((not t.HasField('start') or t.start<=time.time()) and (not t.HasField('end') or t.end>=time.time())):
                    #start = datetime.datetime.fromtimestamp(t.start).strftime('%Y-%m-%d %H:%M:%S')
                    #end = datetime.datetime.fromtimestamp(t.end).strftime('%Y-%m-%d %H:%M:%S')
                    currentTime = int(time.time())
                    start = t.start
                    end = t.end
                    route = []
                    header = ""
                    description = ""

                    for inf in entity.alert.informed_entity:
                        if(inf.HasField('route_id')):
                            route.append(inf.route_id)
                    if(len(route)==0):
                        break
                    route = str(route)[1:-1]

                    if(len(entity.alert.header_text.translation)>0):
                        header = entity.alert.header_text.translation[0].text
                        
                    if(len(entity.alert.description_text.translation)>0):
                        description = entity.alert.description_text.translation[0].text

                    results[count]=[currentTime, start, end, route, header, description]
                    count+=1
                    break

    df = pd.DataFrame.from_dict(results, orient="index", columns=["time", "start", "end", "route", "header", "description"])
    if(writecsv):
        df.to_csv("results.csv")
    return df

fetch('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts', writecsv=True)