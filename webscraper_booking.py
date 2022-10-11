'''
Library to scrap hotel reviews from booking.com and save into CSV
'''

#import 
from audioop import add
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import csv


#define setupchrome function
def setupChrome():
    """This is a function to setup the webdriver to use chrome for automation"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # driver is setup using this arguments
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    return driver

   

#list of URL
urlList = ["https://www.booking.com/hotel/sg/marina-bay-sands.en-gb.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaMkBiAEBmAEJuAEHyAEM2AEB6AEB-AEMiAIBqAIDuAK2rrWZBsACAdICJGVjM2JmNzljLTBjODYtNDA2Yy1iNTQ3LWM2MGQ0ZTgyYzQ1YdgCBuACAQ&sid=06a20784de945644f007f870d6c654ef&dest_id=245881;dest_type=hotel;dist=0;group_adults=2;group_children=0;hapos=1;hpos=1;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1663915874;srpvid=99543030e9b90035;type=total;ucfs=1&#hotelTmpl",
"https://www.booking.com/hotel/my/eq.en-gb.html?aid=7344331&label=metatripad-link-dmetasg-hotel-4674443_xqdz-290eb6344bfdd8c4df9266998aacd714_los-01_bw-012_tod-10_dom-comsg_curr-SGD_gst-02_nrm-01_clkid-65227d7f-fd57-4e4e-af14-5aecc2c57c66_aud-0000_mbl-L_pd-B_sc-2_defdate-1_spo-0_clksrc-0_mcid-10&sid=06a20784de945644f007f870d6c654ef&all_sr_blocks=467444301_341929528_2_2_0;checkin=2022-10-23;checkout=2022-10-24;dest_id=-2403010;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=467444301_341929528_2_2_0;hpos=1;matching_block_id=467444301_341929528_2_2_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=467444301_341929528_2_2_0__83740;srepoch=1665455687;srpvid=ebe21222a020012f;type=total;ucfs=1&#hotelTmpl",
"https://www.booking.com/hotel/it/hotelbaloccoportocervo.en-gb.html?aid=7344331&label=metatripad-link-dmetasg-hotel-81178_xqdz-a4cbed63833673ffbecb3f7d774bfb74_los-01_bw-012_tod-10_dom-com_curr-SGD_gst-02_nrm-01_clkid-daff11c8-747d-4069-ab53-66054247ec1c_aud-0000_mbl-L_pd-B_sc-2_defdate-1_spo-0_clksrc-0_mcid-50&sid=06a20784de945644f007f870d6c654ef&all_sr_blocks=8117801_355349542_2_1_0;checkin=2022-10-23;checkout=2022-10-24;dest_id=900039171;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=8117801_355349542_2_1_0;hpos=1;matching_block_id=8117801_355349542_2_1_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=8117801_355349542_2_1_0__20944;srepoch=1665455798;srpvid=25ec125a33bf008b;type=total;ucfs=1&#hotelTmpl",
"https://www.booking.com/hotel/sg/panpacificsingapore.en-gb.html?label=metatripad-link-dmetasg-hotel-81178_xqdz-a4cbed63833673ffbecb3f7d774bfb74_los-01_bw-012_tod-10_dom-com_curr-SGD_gst-02_nrm-01_clkid-daff11c8-747d-4069-ab53-66054247ec1c_aud-0000_mbl-L_pd-B_sc-2_defdate-1_spo-0_clksrc-0_mcid-50&sid=06a20784de945644f007f870d6c654ef&aid=7344331&ucfs=1&arphpl=1&checkin=2022-10-23&checkout=2022-10-24&dest_id=25086&dest_type=hotel&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=1&hapos=1&sr_order=popularity&srpvid=b8ac1302ec6a0085&srepoch=1665456134&all_sr_blocks=2508615_0_2_1_0&highlighted_blocks=2508615_0_2_1_0&matching_block_id=2508615_0_2_1_0&sr_pri_blocks=2508615_0_2_1_0__34240&tpi_r=1&from_sustainable_property_sr=1&from=searchresults#hotelTmpl",
"https://www.booking.com/hotel/us/sanctuary-new-york.en-gb.html?aid=1288360&label=metagha-link-LUSG-hotel-278666_dev-desktop_los-1_bw-87_dow-Thursday_defdate-1_room-0_gstadt-2_rateid-ig_aud-0_gacid-6644255672_mcid-10_ppa-0_clrid-0_ad-1_gstkid-0_checkin-20230105__lp-2702_r-11275552451425301587&sid=06a20784de945644f007f870d6c654ef&all_sr_blocks=27866612_92515650_0_1_0;checkin=2023-01-05;checkout=2023-01-06;dest_id=20088325;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=27866612_92515650_0_1_0;hpos=1;matching_block_id=27866612_92515650_0_1_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=27866612_92515650_0_1_0__16365;srepoch=1665455664;srpvid=d57112175ab90170;type=total;ucfs=1&#hotelTmpl",
"https://www.booking.com/hotel/sg/hotel-mandarin-oriental.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaMkBiAEBmAEJuAEHyAEM2AEB6AEB-AELiAIBqAIDuALPq5OaBsACAdICJGFmMWU0MTkwLWI5ZGMtNGExNS1iMjQxLTg1MGFjNWFkOGI5MtgCBuACAQ&sid=06a20784de945644f007f870d6c654ef&aid=304142&ucfs=1&arphpl=1&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=1&hapos=1&sr_order=popularity&srpvid=b25811ebbadf0038&srepoch=1665455576&from_sustainable_property_sr=1&from=searchresults#hotelTmpl"]


#defining lists 
hotelname_list = []
address_list = []
review_list = []


#run through loop to perform scrapping for all url's listed
for url in urlList:

   #calling setupchrome function to start
   webdriver = setupChrome()
   webdriver.get(url)

   #retrieving values (hotel name, address and reviews)
   hotelname = webdriver.find_element("xpath", '//h2[@class="d2fee87262 pp-header__title"]').text
   address = webdriver.find_element(by=By.CSS_SELECTOR,value=".hp_address_subtitle.js-hp_address_subtitle.jq_tooltip").text
   review  = webdriver.find_elements(by=By.CSS_SELECTOR,value=".db29ecfbe2.c688f151a2")


   #appending the 3 values to a list for CSV later on
   #reviews.txt
   for x in range(len(review)):
      review_list.append(review[x].text)

   #hotel name list
   for x in range(len(review)):
      hotelname_list += [hotelname]

   #address list 
   for x in range(len(review)):
      address_list += [address]

   #quit driver for every loop
   webdriver.quit()




#convert list to csv
data =list(zip(hotelname_list, address_list, review_list))
reviews = pd.DataFrame(data,columns=['name', 'address', 'review.text'])
reviews.to_csv('hotel_reviews.csv', index=False, header=True)




""" name_list = []
titles_list = [] 
reviews_list = [] 

for i in range(0, 5):
  # Extract reviewer names.

  driver.find_elements(By.XPATH, "(//button[@class='bui-button bui-button--secondary'])")
  names = driver.find_elements(By.XPATH, "(//span[@class='bui-avatar-block__title'])")
  for name in range(len(names)):
    name_list.append(names[name].text)

  time.sleep(2)
  





""" """ # Initialize the SentimentIntensityAnalyzer.
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
plt.tight_layout() """
