import praw
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import json
import pandas as pd
from datetime import datetime
import requests
from psaw import PushshiftAPI
import pandas as pd
import statistics

client_id = '9fjEDY_4zP5gXUKVW9TaNw'
client_secret = 'Imx_uscddEf2AIvMNYlVaan-9RyMxA'
user_agent = 'test'
username = 'Djugi99'
password = 'sxd*y%bgPRNnn3U'

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)

#url='https://api.pushshift.io/reddit/search/submission/?subreddit={}&sort_type=score&sort=desc&after={}&before={}&category=best&size=500'
#post=[]
api = PushshiftAPI(reddit)
#comments = api.search_comments(q='bitcoin',subreddit='bitcoin',before=1648032900,limit=100)
#print(comments)

dates=[]
headlines=[]
authors=[]
subs=[]
ids=[]
scores=[]
permalinks=[]
num_comments=[]
self_texts=[]
names=[]
pols_selftext=[]
pols_title=[]
polarities=[]

konacni=[]
datumi=[]
redovi=[]
sredina_polarity=[]

#start_epoch=int('1655769600')
#pocetak=datetime.utcfromtimestamp(start_epoch).strftime('%Y-%m-%d %H:%M:%S')
#end_epoch=int('1656082800')
#kraj=datetime.utcfromtimestamp(end_epoch).strftime('%Y-%m-%d %H:%M:%S')
sia = SIA()

def mojaFunkcija(subreddit_name, start_time, end_time):
    lks=0
    while(end_time<=1657720800): #13. jul 2022 2:00 pm (po gmt)

        res=list(api.search_submissions(after=start_time,
                                        before=end_time,
                                        subreddit=subreddit_name,
                                        sort='hot',
                                        filter=['url','author', 'title', 'subreddit'],
                                        limit=None))
        broj=0
        for i in range(len(res)):
            if (res[i].title != '[deleted by user]'):
                broj=broj+1
                if(res[i].selftext!='[removed]' and res[i].selftext!='[deleted]' and res[i].selftext!=''):
                    pol_selftext = sia.polarity_scores(res[i].selftext)
                    pol_title = sia.polarity_scores(res[i].title)
                    pol_selftext=pol_selftext['compound']
                    pol_title=pol_title['compound']
                    polarity=(pol_selftext+pol_title)/2
                    pols_title.append(pol_title)
                    pols_selftext.append(pol_selftext)
                else:
                    pol_title = sia.polarity_scores(res[i].title)
                    pol_selftext=0
                    polarity=pol_title['compound']
                    pols_title.append(pol_title['compound'])
                    pols_selftext.append(pol_selftext)
                polarities.append(polarity)

        redovi.append(broj)
        zbir=0

        #for i in range(len(polarities)):
        #    zbir=zbir+polarities[i]
        #ukupno=zbir/len(polarities)
        if len(polarities) > 0:
            ukupno=statistics.mean(polarities)
        else : ukupno=0

        sredina_polarity.append(ukupno)
        if ukupno >= 0.27: ukupno =1
        elif ukupno <= -0.27: ukupno=-1
        else: ukupno = 0
        konacni.append(ukupno)
        datumi.append(datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S'))
        print(datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S'))
        start_time=end_time
        polarities.clear()
        end_time=end_time+3600
        lks=lks+1

pocetak=int('1641528000') #2021-09-25 00:00:00  UVEK GLEDAMO GMT!
kraj=int('1641531600')    #2021-09-25 01:00:00
#print((datetime.utcfromtimestamp(kraj).strftime('%Y-%m-%d %H:%M:%S')))

mojaFunkcija('Dogecoin',pocetak,kraj)
df=pd.DataFrame(
    {
        'Date': datumi,
        'Broj redova':redovi,
        'Polarity': sredina_polarity,
        'Rezultat': konacni
        #'Author': authors,
        #'Score': scores,
        #'Title': headlines,
        #'Self texts': self_texts,
        #'Polarity title': pols_title,
        #'Polarity selftext': pols_selftext,
        #'Polarity': polarities

    }
)
df = df.sort_values(by="Date",ascending=False)
df.to_csv('vaderDoge.csv', header=True, index=False)
print(f'polarities: {polarities}')
