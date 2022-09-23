from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import csv

#url = "https://www.tripadvisor.com/Hotel_Review-g60634-d114075-Reviews-or80-Sheraton_Maui_Resort_Spa-Lahaina_Maui_Hawaii.html"
url = "https://www.tripadvisor.com/Hotel_Review-g294265-d1770798-Reviews-Marina_Bay_Sands-Singapore.html"
#!apt-get update 
#!apt install chromium-chromedriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

driver.get(url)

name_list = []
titles_list = [] 
reviews_list = [] 

for i in range(0, 20):
  # Extract reviewer names.
  names = driver.find_elements(By.XPATH, "(//a[@class='ui_header_link uyyBf'])")
  for name in range(len(names)):
    name_list.append(names[name].text)

  # Extract review title.
  review_names = driver.find_elements(By.XPATH, "(//a[@class='Qwuub']/span)") 
  for review in range(len(review_names)):
    titles_list.append(review_names[review].text)

  # Extract reviews.  
  reviews = driver.find_elements(By.XPATH, "(//q[@class='QewHA H4 _a']/span)") 
  for review in range(len(reviews)):
    reviews_list.append(reviews[review].text)      

  driver.find_element(By.XPATH, "//a[@class='ui_button nav next primary ']").click()
  time.sleep(2)
  
driver.quit()

# Print the lengths of each list.  
print(len(name_list), len(titles_list), len(reviews_list))

data =list( zip(name_list, titles_list, reviews_list))
reviews = pd.DataFrame(data,columns=['Reviewer', 'Review Title', 'Review'])
reviews.head(5)
reviews.to_csv('hotel_reviews.csv', index=False, header=True)
only_reviews = reviews.iloc[:, 2].values
hotel_reviews = pd.DataFrame({'reviews': only_reviews})
hotel_reviews.head(5)

# Initialize the SentimentIntensityAnalyzer.
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
vader = SentimentIntensityAnalyzer()

# Apply lambda function to get compound scores.
function = lambda title: vader.polarity_scores(title)['compound']
hotel_reviews['compound'] = hotel_reviews['reviews'].apply(function)
hotel_reviews.head(5)

from wordcloud import WordCloud
import seaborn as sns
import matplotlib.pyplot as plt

allWords = ' '.join([twts for twts in hotel_reviews['reviews']])
wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)

plt.imshow(wordCloud, interpolation="bilinear")
plt.axis('off')
plt.show()

def getAnalysis(score):
 if score < 0:
    return 'Negative'
 elif score == 0:
    return 'Neutral'
 else:
    return 'Positive'

hotel_reviews['sentiment'] = hotel_reviews['compound'].apply(getAnalysis)

hotel_reviews.head(5)

hotel_reviews['sentiment'].value_counts()

plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
hotel_reviews['sentiment'].value_counts().plot(kind = 'bar')
plt.show()

hotel_reviews.sentiment.value_counts().plot(kind='pie', autopct='%1.0f%%',  fontsize=12, figsize=(9,6), colors=["blue", "red", "yellow"])
plt.ylabel("Hotel Reviews Sentiment", size=14)

plt.figure(figsize=(8, 5))
sns.histplot(hotel_reviews, x='compound', color="darkblue", bins=10, binrange=(-1, 1))
plt.title("Hotel Reviews Sentiment Distribution")
plt.xlabel("Compound Scores")
plt.ylabel("")
plt.tight_layout()
