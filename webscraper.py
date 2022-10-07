"""
This library webscrap hotel reviews from tripadvisor.com and save it into a csv file.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import csv

def setupChrome():
    """This is a function to setup the webdriver to use chrome for automation"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # driver is setup using this arguments
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    return driver

def NEW_tripadvisor_ExtractReview(url):
    """This is a function to extract hotel reviews from tripadvisor with the url of a specific hotel as an argument."""
    # Webdriver is being setup to use chrome
    webdriver = setupChrome()
    # webdriver is going to website via url
    webdriver.get(url)
    # Hotel name is extracted and saved into hotel_name
    hotel_name = webdriver.find_element(By.ID, value="HEADING").text
    # Description of hotel is extracted and saved into variable hotel_description
    hotel_description = webdriver.find_element(By.CSS_SELECTOR, value=".fIrGe._T").text
    # A new csv file is created with these few headings
    df = pd.DataFrame(columns = ['title', 'Date of Stay', 'review'])
    # A for loop that will loop 20 times
    for j in range(0,20):
        time.sleep(2)
        # webdriver to get review boxes and put it in a list
        review_box = webdriver.find_elements(By.XPATH, "//div[@data-reviewid]")
        #rating = webdriver.find_elements(by=By.XPATH, value="//span[contains(@class,'ui_bubble_rating bubble_')]")
        # Looping through the list of review boxes
        for i in review_box:
            # find the title
            title = i.find_element(by=By.CSS_SELECTOR, value='.KgQgP.MC._S.b.S6.H5._a').text  
            # find the review 
            review = i.find_element(by=By.CSS_SELECTOR, value='.fIrGe._T').text 
            #review = i.find_element(By.XPATH, "(//q[@class='QewHA H4 _a']/span)").text.replace("\n", " ")
            # find the date
            date = i.find_element(by=By.CSS_SELECTOR, value=".teHYY._R.Me.S4.H3").text
            # save the title, date and review into csv file
            df.loc[len(df)] = [title, date, review]
        try:
            # Try to find the next button to click to get the next few reviews or else the loop will break
            webdriver.find_element(By.XPATH, "//a[@class='ui_button nav next primary ']").click()
        except ElementClickInterceptedException:
            break
    # replacing the spaces in hotel_name with _
    hotel_name = hotel_name.replace(" ", "_")
    # Naming the CSV file as the hotel name
    df.to_csv(hotel_name + ".csv")
    webdriver.quit()

def airbnb_ExtractReview(url, list1, list2, list3, list4):
    webdriver = setupChrome()
    webdriver.get(url)
    webdriver.find_element(By.XPATH, "//button[@data-testid='pdp-show-all-reviews-button']").click()
    for i in range(0, 20):
        names = webdriver.find_elements(By.XPATH, "//h3[@elementtiming='LCP-target']")
        for name in range(len(names)):
            list1.append(names[name].text)
        
        reviews = webdriver.find_elements(By.XPATH, "//span[@class='ll4r2nl dir dir-ltr']")
        for review in range(len(reviews)):
            list2.append(reviews[review].text)
        
        dates = webdriver.find_elements(By.XPATH, "//li[@class='_1f1oir5']")
        for date in range(len(dates)):
            list3.append(dates[date].split)
    webdriver.quit()
    return list1, list2, list3, list4

def booking_ExtractReview(url , list1, list2, list3, list4):
    
    return list1, list2, list3, list4

def urlchecker(url):
    """This function is used to check the url to see which hotel website it is being used."""
    # If airbnb is being used, then airbnb extract function is used
    if "airbnb" in url:
        print("Feature is coming soon!")
        #airbnb_ExtractReview(url)
    # If tripadvisor is being used, then tripadvisor extract function is used
    elif "tripadvisor" in url:
        NEW_tripadvisor_ExtractReview(url)
    # If booking is being used, then booking extract function is used
    elif "booking" in url:
        print("This feature is coming soon")
        #booking_ExtractReview(url)
    else:
        print("This url is invalid")
          
#urlchecker("https://www.airbnb.com.sg/rooms/38134989?adults=1&children=0&infants=0&check_in=2022-10-09&check_out=2022-10-15&federated_search_id=ac3351c5-d912-4c60-bb85-5f95018d250a&source_impression_id=p3_1664093112_r5qK0mf3BDzW1wCL")
urlchecker("https://www.tripadvisor.com/Hotel_Review-g294265-d1770798-Reviews-Marina_Bay_Sands-Singapore.html")
#urlchecker("https://www.tripadvisor.com/Hotel_Review-g60763-d93525-Reviews-Sanctuary_Hotel_New_York-New_York_City_New_York.html")
#print(len(name_list), len(titles_list), len(reviews_list), len(dates_list), len(ratings_list))


