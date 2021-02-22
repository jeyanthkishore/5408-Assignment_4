import pymongo
import re
from texttable import Texttable
import math
import collections

#establishing connection with database
myclient = pymongo.MongoClient('mongodb+srv://jeyanth:7HPAE8apzyvPmxdV@cluster0.smhz3.mongodb.net/test?authSource=admin&replicaSet=atlas-7myp9l-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true')
databasename='ReuterDb'
spcl_char_regex=re.compile(r'https\S+|([^a-zA-Z\s]+?)')
news_articles = []

database = myclient[databasename]
collection = database["processeddata"]
totaldocuments = 0
#Fetching new articles from the database
for newsdata in collection.find():
   if "data" in newsdata:
        process_data = re.sub(spcl_char_regex,'',str(newsdata['data'].lower()))
        news_articles.append(process_data)
        totaldocuments += 1


keywords = ['canada','hot','rain','cold']

keyword_table = Texttable()
keyword_table.add_row(['TotalDocuments', totaldocuments,'',''])
keyword_table.add_row(['Search Query', 'Document containing term(df)',
            'Total Documents(N)/number of documents term appeared (df)', 'Log10(N/df)'])

count = {}

#Searching for document containing keywords
for keyword in keywords:
    count[keyword] = 0
    for news in news_articles:
        if keyword in news:
            count[keyword] +=1
    keyword_value = totaldocuments/count[keyword]
    keyword_table.add_row([keyword,count[keyword],keyword_value,math.log10(keyword_value)])
print(keyword_table.draw())

canada_table = Texttable()
canada_table.add_row(['Term','Canada',''])
canada_table.add_row(['Canada appeared in '+str(count['canada'])+' documents','Total Words(m)','Frequnecy(f)'])
print(canada_table.draw())

#Searching for frequency of word 'canada' in each document
max_relative_freq = 0
for news in news_articles:
    if 'canada' in news:
        words = news.split()
        individual_words = dict(collections.Counter(words))
        for key,value in individual_words.items():
            if key == 'canada':
                total_words = len(words)
                frequency = value
                canada_table.add_row([news,total_words,frequency])
                relative_frequency = value/len(words)
        if(max_relative_freq<relative_frequency):
            max_relative_freq = relative_frequency
            final_news = news

#Displaying article with high relative frequency
print(canada_table.draw())
print('Highest Relative Frequency : ' +str(max_relative_freq))
print('News Article with Highest Relative Frequency: '+final_news)