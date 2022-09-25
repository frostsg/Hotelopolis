from turtle import title
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

senti = SentimentIntensityAnalyzer()
datafile = pd.read_csv('filtered_datafiniti.csv', encoding='utf-8')
datafile = datafile.astype(str)
# print(datafile)
# nltk.download('vader_lexicon')

reviews = datafile['reviews']
reviews = str(reviews).encode('utf-8')

# datafile['scores'] = datafile['reviews'].apply(lambda reviews:senti.polarity_scores(reviews))
# print(datafile['scores'])

datafile["Positive"] = [senti.polarity_scores(i)["pos"] for i in (datafile["reviews"])]
datafile["Negative"] = [senti.polarity_scores(i)["neg"] for i in (datafile["reviews"])]
datafile["Neutral"] = [senti.polarity_scores(i)["neu"] for i in (datafile["reviews"])]
print(datafile.head())
x = sum(datafile["Positive"])
y = sum(datafile["Negative"])
z = sum(datafile["Neutral"])
#print("Positive score " , round(x), "Negative score ", round(y),"Neutral score ", round(z))

def sentiment_score(pos, neg, neut):
    if (pos > neg) and (pos > neut):
        return("Positive 😊 ")
    elif (neg > pos) and (neg > neut):
        return("Negative 😠 ")
    else:
        return("Neutral 🙂 ")




for i in datafile["hotel"]:
    if datafile["hotel"].all() == datafile["hotel"].all():
        print("Hotel : ",datafile["hotel"][0])
        print("overall review of : ", (sentiment_score(x, y, z)))
        break
    else:
        continue




"""
i=0
for i in datafile["name"]:
    if datafile["name"].all() == datafile["name"].all():
        print("Overall review of: \n")
        print(datafile["name"][0] + "\n")
        i+=1
    else:
        continue"""
# dataset["Positive"] = dataset['reviews'].apply(lambda reviews: sentiments.polarity_scores(str(reviews)))
# dataset["Negative"] = dataset['reviews'].apply(lambda reviews: sentiments.polarity_scores(str(reviews)))
# dataset["Neutral"] = dataset['reviews'].apply(lambda reviews: sentiments.polarity_scores(str(reviews)))

"""
version 1.0 - test - working on hotel.csv only

from turtle import title
import nltk
import pandas
from nltk.sentiment.vader import SentimentIntensityAnalyzer

dataset=pandas.read_csv("C:/Users/anura/OneDrive/Documents/SIT study/INF1002 - Prog Fundamentals\datafiniti_1.csv")
print(dataset.head())

sentiments = SentimentIntensityAnalyzer()
dataset["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in (dataset["title"])]
dataset["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in (dataset["title"])]
dataset["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in (dataset["title"])]
print(dataset.head())

x = sum(dataset["Positive"])
y = sum(dataset["Negative"])
z = sum(dataset["Neutral"])
print(x,y,z)
for i in dataset["hotel"]:
    if dataset["hotel"].all()==dataset["hotel"].all():
        print("Overall review of: \n" )
        print(dataset["hotel"][0] + "\n")
        break
    else:
        continue
    
def sentiment_score(a, b, c):
    if (a>b) and (a>c):
        print("Positive 😊 ")
    elif (b>a) and (b>c):
        print("Negative 😠 ")
    else:
        print("Neutral 🙂 ")
sentiment_score(x, y, z)

"""
