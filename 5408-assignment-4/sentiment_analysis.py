import re
import pymongo
import json
import collections
import pprint
from texttable import Texttable

#Esatblishing connection with database
myclient = pymongo.MongoClient('mongodb+srv://jeyanth:7HPAE8apzyvPmxdV@cluster0.smhz3.mongodb.net/test?authSource=admin&replicaSet=atlas-7myp9l-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true')
databasename ='ProcessedDb'
spcl_char_regex=re.compile('[@_!#$%^&*\\n();,.\'<>?/\|}{~:]')

process_list = []
positive_words = []
negative_words = []

#Fetching tweet data from database
database = myclient[databasename]
collectionname = database["processeddata"]
for data in collectionname.find():
    if "text" in data:
        process_data = re.sub(spcl_char_regex,'',str(data['text'].lower()))
        process_list.append(process_data)

#Fetching data for positive list
with open("positive.txt", "r") as f_obj:
    for line in f_obj:
        positive_words.append(line.strip())

#Fetching data for negative list
with open("negative.txt", "r") as f_obj:
    for line in f_obj:
        negative_words.append(line.strip())


table = Texttable()
table.add_row(['Tweet_Number', 'Text_Message', 'Match_Word', 'Polarity'])

#Checking polarity of the tweet
for index,tweet in enumerate(process_list):
    datalist = tweet.split()
    bag_of_words = dict(collections.Counter(datalist))

    positive = 0
    negative = 0
    match_word = ''
    polarity = 'Neutral'
    for word,word_index in bag_of_words.items():
        if word in positive_words:
            positive = positive+1
            match_word = word
        elif word in negative_words:
            negative = negative+1
            match_word = word

    if positive > negative:
        polarity = "Positive"
    elif negative > positive:
        polarity = "Negative"
    else:
        match_word = ''

    table.add_row([index+1,tweet,match_word,polarity])
    
print(table.draw())