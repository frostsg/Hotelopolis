
from cProfile import label
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from filtering import *

def pos_showWordCloud(review):
  # use tokenize function to use nlp to convert review to list
  keys = tokenize(review)
  keys = [re.sub('[^a-zA-Z]+', '', _) for _ in keys]  # remove numbers or special chaar

  # OPTIONAL - wordcloud including all emotion mentioned in review
  # find common elements from review and all reference lists
  aspects=(list(set(keys).intersection(pos_aspect_list)))
  frequency_dist = nltk.FreqDist(aspects)
  wordcloud = WordCloud().generate_from_frequencies(frequency_dist)
  f = plt.figure("Positive Aspects of this hotel")
  plt.imshow(wordcloud)
  plt.title("What's good about this hotel?")
  plt.axis("off")
  f.show()

def neg_showWordCloud(review):
  # use tokenize function to use nlp to convert review to list
  keys = tokenize(review)
  keys = [re.sub('[^a-zA-Z]+', '', _) for _ in keys]  # remove numbers or special chaar
  # OPTIONAL - wordcloud including all emotion mentioned in review
  # find common elements from review and all reference lists
  aspects=(list(set(keys).intersection(neg_aspect_list)))
  frequency_dist = nltk.FreqDist(aspects)
  wordcloud = WordCloud().generate_from_frequencies(frequency_dist)
  f = plt.figure("Negative Aspects of this hotel")
  plt.imshow(wordcloud)
  plt.title("Where to improve?")
  plt.axis("off")
  f.show()

# Function to create a bar chart with hotel star ratings
def showBarChart(one_star, two_star, three_star, four_star, five_star):
  label = ['One Star', 'Two Stars', 'Three Stars', 'Four Stars', 'Five Stars']
  data = [one_star, two_star, three_star, four_star, five_star]
  g = plt.figure("Hotel Reviews Rating barchart")
  plt.bar(label, data)
  plt.xlabel("Ratings")
  plt.ylabel("No. of Reviews")
  plt.title("Reviews rating")
  g.show()

# Function to create a pie chart with positive and negative reviews
def showPieChart(pos,neg):
  total = pos + neg 
  pos_pe = str(calculatePercentage(pos, total)) + "%"
  neg_pe = str(calculatePercentage(neg, total)) + "%"
  data = [pos, neg]
  color = ['blue','red','grey']
  label = ['Positive Reviews ' + pos_pe, 'Negative Reviews ' + neg_pe]
  y = plt.figure("Percentage of Reviews")
  plt.pie(data, labels=label, colors=color)
  plt.title("Percentage of Reviews")
  y.show()

# Function to calculate percentage
def calculatePercentage(target,total):
  result = (target/total) * 100
  return int(result)

#showPieChart(10,2)
#showBarChart(2,3,4,5,6)
#showWordCloud(doc)

