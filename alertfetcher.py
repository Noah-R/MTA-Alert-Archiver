import requests
import gtfs_realtime_pb2
import time
import datetime
import csv

def fetch(url, writecsv=False):
    r = requests.get(url, headers={'x-api-key': open("key.txt").read()})

    feed=gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(r.content)

    results = []

    for entity in feed.entity:
        if entity.HasField('alert'):
            for t in entity.alert.active_period:
                if((not t.HasField('start') or t.start<=time.time()) and (not t.HasField('end') or t.end>=time.time())):
                    result = {}
                    #start = datetime.datetime.fromtimestamp(t.start).strftime('%Y-%m-%d %H:%M:%S')
                    #end = datetime.datetime.fromtimestamp(t.end).strftime('%Y-%m-%d %H:%M:%S')
                    result['time'] = int(time.time())
                    result['start'] = t.start
                    result['end'] = t.end
                    result['route'] = []
                    result['header'] = ""
                    result['description'] = ""

                    for inf in entity.alert.informed_entity:
                        if(inf.HasField('route_id')):
                            result['route'].append(inf.route_id)
                    if(len(result['route'])==0):
                        break
                    result['route'] = str(result['route'])[1:-1]

                    if(len(entity.alert.header_text.translation)>0):
                        result['header'] = entity.alert.header_text.translation[0].text
                        
                    if(len(entity.alert.description_text.translation)>0):
                        result['description'] = entity.alert.description_text.translation[0].text

                    results.append(result)
                    break


    if(writecsv):
        with open('results.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = results[0].keys(), dialect='unix')
            writer.writeheader()
            writer.writerows(results)
    return results

#fetch('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts', writecsv=True)