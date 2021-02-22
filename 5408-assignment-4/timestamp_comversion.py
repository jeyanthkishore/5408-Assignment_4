import pymongo
import re
import datetime
import csv

#Establishing connection with database
myclient = pymongo.MongoClient('mongodb+srv://jeyanth:7HPAE8apzyvPmxdV@cluster0.smhz3.mongodb.net/test?authSource=admin&replicaSet=atlas-7myp9l-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true')
databasename='ProcessedDb'

process_list = []

database = myclient[databasename]
collectionname = database["processeddata"]

#Conversion of created_at to timestamp and storing it in CSV file
with open('timestamp.csv', 'w', newline='') as file:
    for data in collectionname.find():
        if "created_at" in data:
            print((data['created_at']))
            date_time_obj = datetime.datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S %z %Y')
            timestamp = datetime.datetime.timestamp(date_time_obj)
            print("timestamp =", timestamp)
            writer = csv.writer(file)
            writer.writerow([timestamp])

    

