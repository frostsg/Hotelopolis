"""
This library webscrap hotel reviews from tripadvisor.com and save it into a csv file.
Done by frostsg
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

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
    # Address of hotel is extracted and saved into variable hotel_address
    hotel_address = webdriver.find_element(By.CSS_SELECTOR, ".fHvkI.PTrfg").text
    # A new csv file is created with these few headings
    #df = pd.DataFrame(columns = ['address', 'name', 'reviews.text', 'reviews.rating'])
    df = pd.read_csv("Filtered_Datafiniti_Hotel_Main_Review.csv")
    print(len(df))
    # A for loop that will loop 20 times
    for j in range(0,20):
        time.sleep(2)
        # webdriver to get review boxes and put it in a list
        review_box = webdriver.find_elements(By.XPATH, "//div[@data-reviewid]")
        #rating = webdriver.find_elements(by=By.XPATH, value="//span[contains(@class,'ui_bubble_rating bubble_')]")
        # Looping through the list of review boxes
        for i in review_box:
            # find the review 
            review = i.find_element(by=By.CSS_SELECTOR, value='.fIrGe._T').text 
            # save the title, date and review into csv file
            df.loc[len(df)] = [hotel_address, hotel_name, review, ' ']        
        try:
            webdriver.find_element(By.XPATH, "//a[@class='ui_button nav next primary ']").click()
        except ElementClickInterceptedException:
            break
    # Updating the CSV file 
    df.to_csv("Filtered_Datafiniti_Hotel_Main_Review.csv", index=False)
    # Stopping the webdriver
    webdriver.quit()

def booking_ExtractReview(url):
     # Webdriver is being setup to use chrome
    webdriver = setupChrome()
    # webdriver is going to website via url
    webdriver.get(url)
    hotel_name = webdriver.find_element("xpath", '//h2[@class="d2fee87262 pp-header__title"]').text
    hotel_address = webdriver.find_element(by=By.CSS_SELECTOR,value=".hp_address_subtitle.js-hp_address_subtitle.jq_tooltip").text
    reviews  = webdriver.find_elements(by=By.CSS_SELECTOR,value=".db29ecfbe2.c688f151a2")
    df = pd.read_csv("Filtered_Datafiniti_Hotel_Main_Review.csv")
    for i in reviews:
        review = i.text
        df.loc[len(df)] = [hotel_address, hotel_name, review, ' ']
    # Updating the CSV file 
    df.to_csv("Filtered_Datafiniti_Hotel_Main_Review.csv", index=False)
    # Stopping the webdriver
    webdriver.quit()

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
        booking_ExtractReview(url)
    else:
        print("This url is invalid")
          
          

#urlchecker("https://www.tripadvisor.com/Hotel_Review-g298570-d555433-Reviews-Hilton_Kuala_Lumpur-Kuala_Lumpur_Wilayah_Persekutuan.html")
#urlchecker("https://www.tripadvisor.com.sg/Hotel_Review-g298570-d12621892-Reviews-EQ_Kuala_Lumpur-Kuala_Lumpur_Wilayah_Persekutuan.html")
#urlchecker("https://www.tripadvisor.com/Hotel_Review-g60763-d93525-Reviews-Sanctuary_Hotel_New_York-New_York_City_New_York.html")
#urlchecker("https://www.tripadvisor.com/Hotel_Review-g294265-d1770798-Reviews-Marina_Bay_Sands-Singapore.html")
#urlchecker("https://www.tripadvisor.com/Hotel_Review-g194856-d498287-Reviews-Hotel_Balocco-Porto_Cervo_Arzachena_Province_of_Olbia_Tempio_Sardinia.html")
#urlchecker("https://www.tripadvisor.com.sg/Hotel_Review-g294265-d302294-Reviews-Pan_Pacific_Singapore-Singapore.html")
#urlchecker("https://www.tripadvisor.com/Hotel_Review-g294265-d301468-Reviews-or3905-Mandarin_Oriental_Singapore-Singapore.html")
#urlchecker("https://www.booking.com/hotel/sg/marina-bay-sands.en-gb.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaMkBiAEBmAEJuAEHyAEM2AEB6AEB-AEMiAIBqAIDuAK2rrWZBsACAdICJGVjM2JmNzljLTBjODYtNDA2Yy1iNTQ3LWM2MGQ0ZTgyYzQ1YdgCBuACAQ&sid=06a20784de945644f007f870d6c654ef&dest_id=245881;dest_type=hotel;dist=0;group_adults=2;group_children=0;hapos=1;hpos=1;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1663915874;srpvid=99543030e9b90035;type=total;ucfs=1&#hotelTmpl")
#urlchecker("https://www.booking.com/hotel/sg/panpacificsingapore.en-gb.html?aid=7344331&label=metatripad-link-dmetasg-hotel-81178_xqdz-a4cbed63833673ffbecb3f7d774bfb74_los-01_bw-012_tod-10_dom-com_curr-SGD_gst-02_nrm-01_clkid-daff11c8-747d-4069-ab53-66054247ec1c_aud-0000_mbl-L_pd-B_sc-2_defdate-1_spo-0_clksrc-0_mcid-50&sid=48e4a0bb292823a36874e7f13da081b9&all_sr_blocks=2508615_0_2_1_0;checkin=2022-10-23;checkout=2022-10-24;dest_id=25086;dest_type=hotel;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=2508615_0_2_1_0;hpos=1;matching_block_id=2508615_0_2_1_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=2508615_0_2_1_0__34240;srepoch=1665456134;srpvid=b8ac1302ec6a0085;type=total;ucfs=1&#hotelTmpl")
#urlchecker("https://www.booking.com/hotel/my/eq.en-gb.html?aid=7344331&label=metatripad-link-dmetasg-hotel-4674443_xqdz-290eb6344bfdd8c4df9266998aacd714_los-01_bw-012_tod-10_dom-comsg_curr-SGD_gst-02_nrm-01_clkid-65227d7f-fd57-4e4e-af14-5aecc2c57c66_aud-0000_mbl-L_pd-B_sc-2_defdate-1_spo-0_clksrc-0_mcid-10&sid=06a20784de945644f007f870d6c654ef&all_sr_blocks=467444301_341929528_2_2_0;checkin=2022-10-23;checkout=2022-10-24;dest_id=-2403010;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=467444301_341929528_2_2_0;hpos=1;matching_block_id=467444301_341929528_2_2_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=467444301_341929528_2_2_0__83740;srepoch=1665455687;srpvid=ebe21222a020012f;type=total;ucfs=1&#hotelTmpl")
#urlchecker("https://www.booking.com/hotel/us/sanctuary-new-york.en-gb.html?aid=1288360&label=metagha-link-LUSG-hotel-278666_dev-desktop_los-1_bw-87_dow-Thursday_defdate-1_room-0_gstadt-2_rateid-ig_aud-0_gacid-6644255672_mcid-10_ppa-0_clrid-0_ad-1_gstkid-0_checkin-20230105__lp-2702_r-11275552451425301587&sid=06a20784de945644f007f870d6c654ef&all_sr_blocks=27866612_92515650_0_1_0;checkin=2023-01-05;checkout=2023-01-06;dest_id=20088325;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=27866612_92515650_0_1_0;hpos=1;matching_block_id=27866612_92515650_0_1_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=27866612_92515650_0_1_0__16365;srepoch=1665455664;srpvid=d57112175ab90170;type=total;ucfs=1&#hotelTmpl")
#urlchecker("https://www.booking.com/hotel/sg/hotel-mandarin-oriental.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaMkBiAEBmAEJuAEHyAEM2AEB6AEB-AELiAIBqAIDuALPq5OaBsACAdICJGFmMWU0MTkwLWI5ZGMtNGExNS1iMjQxLTg1MGFjNWFkOGI5MtgCBuACAQ&sid=06a20784de945644f007f870d6c654ef&aid=304142&ucfs=1&arphpl=1&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=1&hapos=1&sr_order=popularity&srpvid=b25811ebbadf0038&srepoch=1665455576&from_sustainable_property_sr=1&from=searchresults#hotelTmpl")