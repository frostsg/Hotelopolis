from tkinter import *
import math
import pandas
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os.path
from Scripts.filtering import *
from Scripts.webscraper import *
from PIL import ImageTk, Image
from Scripts.review_analysis import *

##########Initialise values############
window = Tk()
HotelCSVData = pd.read_csv("Filtered_Datafiniti_Hotel_Main_Review.csv")
window.geometry("1920x1080")
window.option_add("*Background", "#fff6ec")
window.title("Hotelopolis")
window.iconbitmap("icon/hotelopolis.ico")
senti = SentimentIntensityAnalyzer()
#image = ImageTk.PhotoImage(Image.open("icon/hotelopolis.png"))

Framecolor = "#DAA06D" #color for all frames

#list of hotels on menu (button form)
HotelMenuList=[]
#list of hotels taken from csv
HotelsList =[]
#list of recommended hotels at the side when user clicks hotels
RecommendedHotelsList=[]
#list of bookmarked hotel objects to access class
BookmarkedHotelsObjectsList=[]
#list of bookmarked hotels for dropdown menu
BookmarkedHotelsNameList=[]
#list of review items
ReviewItemsList=[]


#for writing bookmarks
Bookmarkdata=None #if file exists, read from it

#original hotel options
HotelOptions=[]
for name in HotelCSVData["name"]: #add all hotels in csv
    if(pd.isnull(name)): #get rid of any null cells
       continue
    if(name not in HotelOptions):#as the name is repeated multiple times in csv, just take one
        HotelOptions.append(name)

#options for sorting in dropdown menu
MainMenuSortOptions = [
    'Alphabetical A-Z',
    'Alphabetical Z-A',
    'Rating (High to Low)',
    'Rating (Low to High)'
    ]

#options for review filtering
ReviewFilterOptions=[
    'All',
    '1 star',
    '2 stars',
    '3 stars',
    '4 stars',
    '5 stars'
]

def UpdateBookmarkCsv(toggledhotel = None):
    if(toggledhotel == None):
        if(os.path.exists("Bookmarks.csv")):
            Bookmarkdata = pd.read_csv("Bookmarks.csv", index_col=0)
            listofbookmarks = list(Bookmarkdata['name'])
            if(len(HotelOptions) > len(listofbookmarks)):
                NewHotels = [hotel for hotel in HotelOptions if hotel not in listofbookmarks]#check for new hotel and add if neccessary
                BookmarkDataFrame = pd.DataFrame(NewHotels, columns=['name'])
                BookmarkDataFrame["bookmarked"] = False
                Bookmarkdata = pandas.concat([Bookmarkdata, BookmarkDataFrame],axis=0, ignore_index=True)
                Bookmarkdata.to_csv("Bookmarks.csv")

            elif(len(HotelOptions) < len(listofbookmarks)):
                OldHotels = [hotel for hotel in listofbookmarks if hotel not in HotelOptions]  # check for new hotel and add if neccessary
                for hotel in OldHotels:
                    Bookmarkdata.drop(Bookmarkdata[Bookmarkdata['name'] == hotel].index, inplace=True)
                    Bookmarkdata.to_csv("Bookmarks.csv")
        else:
            BookmarkDataFrame = pd.DataFrame(HotelOptions, columns=['name'])  #since bookmarked csv not created, create one and set all hotels to not bookmarked
            BookmarkDataFrame["bookmarked"] = False
            BookmarkDataFrame.to_csv("Bookmarks.csv")

    else:
        Bookmarkdata = pd.read_csv("Bookmarks.csv")
        Bookmarkdata.loc[Bookmarkdata.name == toggledhotel.Name, "bookmarked"] = toggledhotel.Bookmarked
        Bookmarkdata.to_csv("Bookmarks.csv", index=False)  # update csv based on new bookmarks

    Bookmarkdata = pd.read_csv("Bookmarks.csv", index_col=0)
    return Bookmarkdata


class Hotel:
    def __init__(self, name, address, scoreslist, reviewslist, bookmarked): #initialise hotel objects
        self.Name = name
        self.Address = address
        self.ScoresList = scoreslist
        self.ReviewsList = reviewslist
        self.Bookmarked = bookmarked

        #get sentimental anayisis of hotel reviews
        analysis ={}
        analysis["Positive"] = [senti.polarity_scores(i)["pos"] for i in self.ReviewsList]
        analysis["Negative"] = [senti.polarity_scores(i)["neg"] for i in self.ReviewsList]

        TotalScore = 0.00
        if(' ' in self.ScoresList): #detect for hotels without given score and use sentimental analysis score to get review score
            PositiveList = list(analysis["Positive"])
            NegativeList = list(analysis["Negative"])
            for index, values in enumerate(PositiveList):
                totalratingadded = PositiveList[index] + NegativeList[index]
                if(totalratingadded !=0):
                    calculated = round((PositiveList[index]/totalratingadded) * 5) #calculated score by adding positive and negative then divide by total, times 5(out of 5 stars)
                    if(calculated == 0): #to make completely negative reviews have a score of 1
                        calculated=1
                    self.ScoresList[index] = calculated
                    TotalScore += calculated
                else:#if review is completely neutral, give it a score of 3
                    calculated = 3
                    self.ScoresList[index] = calculated
                    TotalScore += calculated
        else:
            for rating in self.ScoresList:
                TotalScore += int(rating)

        self.AverageScore = TotalScore / len(self.ScoresList) #calculate average score by adding all reviews score and divide by number of reviews

        self.Facilities = facility_check(','.join(reviewslist)) #get facilities of hotel from finding keywords from reviews

        GoodReviewsList=[]
        BadReviewsList = []
        for index, score in enumerate(self.ScoresList):
            if(int(score) >=4):
                GoodReviewsList.append(self.ReviewsList[index])
            if (int(score) <= 3):
                BadReviewsList.append(self.ReviewsList[index])

        self.pos_WordCloudReview = ','.join(GoodReviewsList)
        self.neg_WordCloudReview = ','.join(BadReviewsList)


#################functions#####################
def ClearMainMenu(): #clear all widgets on main menu
    MainMenuFrame.grid_forget()
    FilterFrame.grid_forget()

def ClearHotelDetails(): #clear all widgets on hotel details
    RecommendationFrame.grid_forget()
    HotelDetailsFrame.grid_forget()
    MenuButton.grid_forget()
    for Review in ReviewItemsList:
        Review.destroy()

    ReviewItemsList.clear()

def RefreshHotels():
    HotelCSVData = pd.read_csv("Filtered_Datafiniti_Hotel_Main_Review.csv")

    for name in HotelCSVData["name"]:
        if name not in HotelOptions:
            ReviewsList = list(HotelCSVData.loc[HotelCSVData.name == name, 'reviews.text'])
            ReviewsRating = list(HotelCSVData.loc[HotelCSVData.name == name, 'reviews.rating'])
            AddressList = HotelCSVData.loc[HotelCSVData.name == name, 'address']
            Address = AddressList.iat[0]
            Bookmarked = False
            HotelObject = Hotel(name, Address, ReviewsRating, ReviewsList, Bookmarked)
            HotelsList.append(HotelObject)
            HotelOptions.append(name)

    UpdateBookmarkCsv()
    # sort and filter main menu based on default values
    FilterAndSortHotelDetails(SortVariable)


def ToggleBookmark(): #toggle bookmarked status of current hotel
    currenthotelname = HotelNameLabel.cget("text")
    for hotel in HotelsList:
        if(hotel.Name == currenthotelname):
            hotel.Bookmarked = BookmarkedVariable.get()
            if(hotel.Bookmarked):
                BookmarkedHotelsNameList.append(hotel.Name)
                BookmarkedHotelsObjectsList.append(hotel)
                if ("No Bookmarks") in BookmarkedHotelsNameList:
                    BookmarkedHotelsNameList.remove("No Bookmarks")
            else:
                BookmarkedHotelsNameList.remove(hotel.Name)
                BookmarkedHotelsObjectsList.remove(hotel)
                if(len(BookmarkedHotelsNameList)==0):
                    BookmarkedHotelsNameList.append("No Bookmarks")

            UpdateBookmarkCsv(hotel)

    BookmarkDropdown["menu"].delete(0, 'end')
    for hotel in BookmarkedHotelsNameList:
        BookmarkDropdown["menu"].add_command(label= hotel, command=lambda hotel = hotel:SelectFromBookmark(hotel))  #update bookmark dropdown

def FilterAndSortHotelDetails(sortoption = None): #update main menu based on filter and sort options
    for HotelButton in HotelMenuList: #destroy all buttons as we will create them based on all the filter and sort options
        HotelButton.destroy()

    HotelMenuList.clear() #clear list of hotel buttons as they all are destroyed

    #create list to check which ameneties user selected
    amenetiesselectedlist = []
    if(restaurant.get() != "na"):
        amenetiesselectedlist.append(restaurant.get())
    if (pool.get() != "na"):
        amenetiesselectedlist.append(pool.get())
    if (jacuzzi.get() != "na"):
        amenetiesselectedlist.append(jacuzzi.get())
    if(gym.get()!="na"):
        amenetiesselectedlist.append(gym.get())
    if (spa.get() != "na"):
        amenetiesselectedlist.append(spa.get())

    #sort list to be displayed based on user selected sort
    if(SortVariable.get() == 'Alphabetical A-Z'):
        SortedList = sorted(HotelsList, key= lambda x:x.Name)
    elif(SortVariable.get() == 'Alphabetical Z-A'):
        SortedList = sorted(HotelsList, key= lambda x:x.Name, reverse=True)
    elif (SortVariable.get() == 'Rating (High to Low)'):
        SortedList = sorted(HotelsList, key=lambda x: x.AverageScore, reverse=True)
    elif (SortVariable.get() == 'Rating (Low to High)'):
        SortedList = sorted(HotelsList, key=lambda x: x.AverageScore)


    #create buttons based on sorted list, ameneties selected and filtering options
    if(onestar.get() == 0 and twostar.get() == 0 and threestar.get() == 0 and fourstar.get() == 0 and fivestar.get() == 0): #if no star filter selected
        for index, hotel in enumerate(SortedList):
            if (len(amenetiesselectedlist) > 0 and not any(x in hotel.Facilities for x in amenetiesselectedlist)): #if hotel does not have selected ameneites, skip it and dont create a button
                continue
            MenuHotelFrame = Frame(master=MainMenuFrame, highlightthickness=2, highlightbackground=Framecolor)
            MenuHotelFrame.grid(row=index + 1, column=0, sticky=N, pady=10, padx=10)
            facilitieslist = ', '.join(hotel.Facilities)
            HotelPicture =  Label(MenuHotelFrame, text="Insert pic", anchor=CENTER)
            HotelPicture.grid(row=0, column=0, sticky=W, padx=10)
            HotelButton = Button(MenuHotelFrame, text=hotel.Name + "\n"+hotel.Address + "\n Average Score: %0.1f/5" % hotel.AverageScore + "\n Facilities: " + facilitieslist,
                                     command=lambda hotel=hotel: DisplayHotelDetails(hotel), width=60, height=6, font=("Arial", 10), relief=GROOVE)
            HotelButton.grid(row=0, column=1, sticky=W)
            HotelMenuList.append(MenuHotelFrame) #add hotel button back into list
    else:
        for index, hotel in enumerate(SortedList): #else if star filter selected, create buttons based on star filter
            if (len(amenetiesselectedlist) > 0 and not any(x in hotel.Facilities for x in amenetiesselectedlist)): #if hotel does not have selected ameneites, skip it and dont create a button
                continue
            if(int(hotel.AverageScore) == onestar.get() or int(hotel.AverageScore) == twostar.get() or int(hotel.AverageScore) == threestar.get() or int(hotel.AverageScore) == fourstar.get() or int(hotel.AverageScore) == fivestar.get()):
                MenuHotelFrame = Frame(master=MainMenuFrame, highlightthickness=2, highlightbackground=Framecolor)
                MenuHotelFrame.grid(row=index + 1, column=0, sticky=N, pady=10, padx=10)
                facilitieslist = ', '.join(hotel.Facilities)
                HotelPicture = Label(MenuHotelFrame, text="Insert pic", anchor=CENTER)
                HotelPicture.grid(row=0, column=0, sticky=W, padx=10)
                HotelButton = Button(MenuHotelFrame,
                                     text=hotel.Name + "\n" + hotel.Address + "\n Average Score: %0.1f/5" % hotel.AverageScore + "\n Facilities: " + facilitieslist,
                                     command=lambda hotel=hotel: DisplayHotelDetails(hotel), width=60, height=6,
                                     font=("Arial", 10), relief=GROOVE)
                HotelButton.grid(row=0, column=1, sticky=W)
                HotelMenuList.append(MenuHotelFrame)  # add hotel button back into list


    #show no results label if completely empty
    if(len(HotelMenuList) == 0):
        Emptylabel.grid(row= 1, column=0, sticky=N, pady=10)
    else:
        Emptylabel.grid_forget()#clear no result label if there are hotels to display

    UpdateScrollbar()

def SelectFromBookmark(selectedbookmark): #called when u select a hotel from the bookmark dropdown. It will call displayhoteldetails function based on selection
    for hotel in BookmarkedHotelsObjectsList:
        if(hotel.Name == selectedbookmark):
            DisplayHotelDetails(hotel)
            break
    BookmarkNameVariable.set("Bookmarks") #reset bookmark dropdown title

def DisplayWorldCloud():
    currenthotel = None
    currenthotelname = HotelNameLabel.cget("text")
    for hotel in HotelsList:
        if (hotel.Name == currenthotelname):
            currenthotel = hotel

    neg_showWordCloud(currenthotel.neg_WordCloudReview, currenthotelname)
    pos_showWordCloud(currenthotel.pos_WordCloudReview, currenthotelname)
    
    

def UpdateRecommendations(hotel): #display recommendations at side of hotel details
    for HotelButton in RecommendedHotelsList: #destroy all buttons recommended before to refresh with new ones
        HotelButton.destroy()

    RecommendedHotelsList.clear()
    for index, otherhotel in enumerate(HotelsList):
        facilitieslist = ', '.join(otherhotel.Facilities)
        if (math.ceil(otherhotel.AverageScore) >= round(hotel.AverageScore) and otherhotel.Name != hotel.Name): #check for hotels with similar of higher star ratings to recommend
            RecoHotelFrame = Frame(master=RecommendationFrame, highlightthickness=2, highlightbackground=Framecolor)
            RecoHotelFrame.grid(row=index + 1, column=0, sticky=N, pady=10, padx=10)
            RecoHotelPicture =  Label(RecoHotelFrame, text="Insert pic", anchor=CENTER)
            RecoHotelPicture.grid(row=0, column=0, sticky=W, padx=10)
            RecoHotelMenuButton = Button(RecoHotelFrame, text=otherhotel.Name + "\n Average Score: %0.1f/5" % otherhotel.AverageScore + "\n Facilities: " + facilitieslist,
                                     command=lambda otherhotel=otherhotel: DisplayHotelDetails(otherhotel), width=26, height=6, font=("Arial", 10), relief=GROOVE, wraplength=200)
            RecoHotelMenuButton.grid(row=0, column=1, sticky=N)
            RecommendedHotelsList.append(RecoHotelFrame)

def FilterReviews(filterby):
    for item in ReviewItemsList:
        item.destroy()
    ReviewItemsList.clear()

    currenthotel = None
    currenthotelname = HotelNameLabel.cget("text")
    for hotel in HotelsList:
        if (hotel.Name == currenthotelname):
            currenthotel = hotel

    filteredvar = 0
    if(filterby == "1 star"):
        filteredvar = 1
    elif(filterby == "2 stars"):
        filteredvar = 2
    elif (filterby == "3 stars"):
        filteredvar = 3
    elif (filterby == "4 stars"):
        filteredvar = 4
    elif (filterby == "5 stars"):
        filteredvar = 5

    # display reviews
    for index, score in enumerate(currenthotel.ScoresList):
        if(filteredvar!= 0 and filteredvar != int(score)):
            continue
        ReviewTextFrame = Frame(master=HotelReviewFrame, highlightbackground=Framecolor, highlightthickness=1)
        ReviewTextFrame.grid(row=index + 2, column=0, sticky=NSEW, pady=5)
        ReviewsScoreText = Label(ReviewTextFrame, text=("Score:", score))
        ReviewsScoreText.grid(row=index, column=0, sticky=NW)
        ReviewsText = Label(ReviewTextFrame, text=currenthotel.ReviewsList[index], justify=LEFT, wraplength=800)
        ReviewsText.grid(row=index + 1, column=0, sticky=NW)
        ReviewItemsList.append(ReviewTextFrame)

# Function to create a bar chart for reviews based on their stars rating 
def DisplayBarChart():
    # Getting current hotel 
    currenthotel = None
    currenthotelname = HotelNameLabel.cget("text")
    for hotel in HotelsList:
        if (hotel.Name == currenthotelname):
            currenthotel = hotel
            
    # Categorizing reviews based on their ratings
    one_count, two_count, three_count, four_count, five_count = 0,0,0,0,0
    for score in currenthotel.ScoresList:
        if int(score) == 5:
            five_count += 1
        elif int(score) == 4:
            four_count += 1
        elif int(score) == 3:
            three_count += 1
        elif int(score) == 2:
            two_count += 1
        else:
            one_count += 1
            
    # Displaying bar chart function from analysis
    showBarChart(one_count, two_count, three_count, four_count, five_count, currenthotelname)

# Function to create and display a pie chart
def DisplayPieChart():
    currenthotel = None
    currenthotelname = HotelNameLabel.cget("text")
    for hotel in HotelsList:
        if (hotel.Name == currenthotelname):
            currenthotel = hotel
    
    analysis ={}
    analysis["Positive"] = [senti.polarity_scores(i)["pos"] for i in currenthotel.ReviewsList]
    analysis["Negative"] = [senti.polarity_scores(i)["neg"] for i in currenthotel.ReviewsList]
    positive = sum(analysis["Positive"])
    negative = sum(analysis["Negative"])
    showPieChart(positive, negative, currenthotelname)

# Function for Show Analysis Button to display WordCloud, Bar Chart and Pie Chart
def showAnalysis():
    DisplayBarChart()
    DisplayPieChart()

def showEmotions():
    DisplayWorldCloud()

def UpdateScrollbar():
    # scrollbar
    # update size of content for scrollbar
    MainCanvas.update_idletasks()
    MainCanvas.config(scrollregion=MainCanvas.bbox("all"))
    # reset scrollbar position to start
    MainCanvas.xview_moveto(0)
    MainCanvas.yview_moveto(0)

def DisplayMainMenu():
    ClearHotelDetails() #clear hoteldetails gui and show main menu gui
    FilterFrame.grid(row=1, column=0, sticky=N, padx=40)
    MainMenuFrame.grid(row=1, column=1, sticky=NSEW)
    UpdateScrollbar()

#logic for UI display, it clears details and reformats it for the new hotel
def DisplayHotelDetails(hotel):
    ClearHotelDetails() #clear details of old displayed hotel as we will update new one with new widgets
    ClearMainMenu() #clear main menu

    #configure hotel name label
    HotelNameLabel.config(text=hotel.Name)

    # configure hotel address label
    AddressLabel.config(text=("Address: " + hotel.Address))

    facilitieslist = ', '.join(hotel.Facilities)
    FacilitiesLabel.config(text=("Facilities: " + facilitieslist))

    # configure bookmarked status of hotel
    BookmarkedVariable.set(hotel.Bookmarked)

    # configure hotel average score /5
    AverageScoreLabel.config(text= "Star Rating: %0.1f"%hotel.AverageScore+ "/5")

    #configure images
    HotelMainImage.config(text="Main Image")
    HotelSmallImageOne.config(text="Small Image")
    HotelSmallImageTwo.config(text="Small Image")
    HotelSmallImageThree.config(text="Small Image")

    ReviewFilterVariable.set(ReviewFilterOptions[0])

    #display reviews
    for index, score in enumerate(hotel.ScoresList):
        ReviewTextFrame = Frame(master=HotelReviewFrame, highlightbackground=Framecolor, highlightthickness=1)
        ReviewTextFrame.grid(row=index +2, column=0, sticky=NSEW, pady=5)
        ReviewsScoreText = Label(ReviewTextFrame, text=("Score:",score))
        ReviewsScoreText.grid(row=index, column=0, sticky=NW)
        ReviewsText = Label(ReviewTextFrame, text=hotel.ReviewsList[index], justify=LEFT, wraplength=800)
        ReviewsText.grid(row=index+1, column=0, sticky=NW)
        ReviewItemsList.append(ReviewTextFrame)


    UpdateRecommendations(hotel) #call update recommendations to show hotels with similar or better ratings
    #show widgets needed for hotel details
    RecommendationFrame.grid(row=1, column=0, padx=40, sticky=N)
    HotelDetailsFrame.grid(row=1, column=1, sticky=N)
    MenuButton.grid(row=0, column=0, padx=35, pady=20, sticky=NE)
    UpdateScrollbar()

## Create a add hotel pop up 
def open_popup():
    global top
    top = Toplevel(MainFrame)
    top.geometry("500x150")
    top.title("Add hotel")
    Label(top, text= "Enter the url of the hotel below! (Tripadvisor.com or booking.com)", font=('Arial')).grid(row=0,column=3)
    global input_text
    input_text = Entry(top, width=40, textvariable="url")
    input_text.focus_set()
    input_text.grid(row=2, column=3)
    #input_text = Text(top, height=3, width=50)
    #input_text.grid(row=2, column=3)
    Ok_button = Button(top, text = "Ok add it!", command= take_input)
    Ok_button.grid(row=3, column=3)
    

## Take string input and start webscrapping
def take_input(*args):
    url = input_text.get() 
    print(url)
    urlchecker(url)
    top.destroy()
    RefreshHotels()

## Click on button
def on_button():
    take_input()

#####Main code#####
Bookmarkdata = UpdateBookmarkCsv()
#Bookmarkdata = pd.read_csv("Bookmarks.csv", index_col=0)
for i in HotelOptions:
    #create hotels
    ReviewsList = list(HotelCSVData.loc[HotelCSVData.name == i, 'reviews.text'])
    ReviewsRating = list(HotelCSVData.loc[HotelCSVData.name == i, 'reviews.rating'])
    AddressList =  HotelCSVData.loc[HotelCSVData.name == i, 'address']
    Address = AddressList.iat[0]
    Bookmarked = Bookmarkdata.loc[Bookmarkdata.name == i, 'bookmarked'].bool()
    HotelObject = Hotel(i, Address, ReviewsRating, ReviewsList, Bookmarked)
    HotelsList.append(HotelObject)
    if(Bookmarked == True):
        BookmarkedHotelsObjectsList.append(HotelObject)
        BookmarkedHotelsNameList.append(HotelObject.Name)




##########UI LAYOUT##########
#frame for entire window
MainFrame = Frame(master=window)
MainFrame.pack(side=LEFT, fill=BOTH, expand=1)

#canvas for everything
MainCanvas = Canvas(master=MainFrame)
VScrollbar = Scrollbar(master=MainFrame, orient=VERTICAL, command=MainCanvas.yview)
HScrollbar = Scrollbar(master=MainFrame, orient=HORIZONTAL, command=MainCanvas.xview)
#scrollbar
VScrollbar.pack(side=RIGHT, fill=Y)
HScrollbar.pack(side=BOTTOM, fill=X)

#Frame for everything
ContentFrame= Frame(MainCanvas)
MainCanvas.create_window((0,0), window=ContentFrame, anchor=NW)
MainCanvas.configure(xscrollcommand=HScrollbar.set, yscrollcommand=VScrollbar.set)
MainCanvas.pack(side=LEFT, fill=BOTH, expand=1)

#App Title
AppTitleLabel = Label(ContentFrame, text="HOTELOPOLIS", font=("Arial", 40), anchor=CENTER)
AppTitleLabel.grid(row=0, column=1)

#Filter frame for filtering hotels
# Function for scrolling using mouse wheel
def _on_mouse_wheel(event):
    MainCanvas.yview_scroll(-1 * int((event.delta / 120)), "units")

#Mouse Wheel scrolling implementation
MainCanvas.configure(yscrollcommand=VScrollbar.set)
MainCanvas.bind('<Configure>', lambda e: MainCanvas.configure(scrollregion = MainCanvas.bbox("all")))
MainCanvas.bind_all("<MouseWheel>", _on_mouse_wheel)

#Filter Frame
FilterFrame = Frame(master=ContentFrame, highlightbackground=Framecolor, highlightthickness=1, padx=10, pady=5)

#Recommendation frame for recommended hotels
RecommendationFrame = Frame(master=ContentFrame, highlightbackground=Framecolor, highlightthickness=1,padx=10, pady=5)

#Frame for hotel buttons, hotel info
MainMenuFrame = Frame(master=ContentFrame)

#Frame for hotel details
HotelDetailsFrame = Frame(master=ContentFrame, highlightbackground=Framecolor, highlightthickness=1,padx=10, pady=5)

#Frame for display of hotel name, and bookmark and address
HotelDescriptionFrame = Frame(master=HotelDetailsFrame)
HotelDescriptionFrame.grid(row=0, column=0, sticky=NW)

#Frame for display of hotel name, and bookmark
HotelNameFrame = Frame(master=HotelDescriptionFrame)
HotelNameFrame.grid(row=0, column=0, sticky=NW)

#Frame for reviews
HotelPicturesFrame =  Frame(master=HotelDetailsFrame, highlightbackground=Framecolor, highlightthickness=1, padx=10, pady=5)
HotelPicturesFrame.grid(row=1, column=0, sticky=NSEW)

#Frame for main picture
HotelMainPictureFrame =  Frame(master=HotelPicturesFrame, padx=10)
HotelMainPictureFrame.grid(row=0, column=0, sticky=NW)

#Frame for small pictures
HotelSmallPicturesFrame =  Frame(master=HotelPicturesFrame)
HotelSmallPicturesFrame.grid(row=0, column=1, sticky=NW)

#Hotel Main Image Label
HotelMainImage = Label(HotelMainPictureFrame, text="Main pic", width=30, height=20, highlightbackground=Framecolor, highlightthickness=1, padx=10, pady=10)
HotelMainImage.grid(row=0, column=0)

#Hotel Main Image Label
HotelSmallImageOne = Label(HotelSmallPicturesFrame, text="small pic", width=10, height=10, highlightbackground=Framecolor, highlightthickness=1, padx=10, pady=10)
HotelSmallImageOne.grid(row=0, column=0)

#Hotel Main Image Label
HotelSmallImageTwo = Label(HotelSmallPicturesFrame, text="small pic", width=10, height=10, highlightbackground=Framecolor, highlightthickness=1, padx=10, pady=10)
HotelSmallImageTwo.grid(row=1, column=0)

#Hotel Main Image Label
HotelSmallImageThree = Label(HotelSmallPicturesFrame, text="small pic", width=10, height=10, highlightbackground=Framecolor, highlightthickness=1, padx=10, pady=10)
HotelSmallImageThree.grid(row=1, column=1)

#Frame for reviews
HotelReviewFrame =  Frame(master=HotelDetailsFrame)
HotelReviewFrame.grid(row=2, column=0, sticky=NW)

#Recommendation Label
RecommendationLabel = Label(RecommendationFrame, text="You may also like:")
RecommendationLabel.grid(row=0, column=0)

#Back to menu Button
MenuButton = Button(ContentFrame, text="Back To Menu", command=DisplayMainMenu,font=("Arial", 10), relief=GROOVE)

#Hotel name label in display hotel options
HotelNameLabel = Label(HotelNameFrame, font=("Arial", 30))
HotelNameLabel.grid(row=0, column=0, sticky=NW)

#Address label in display hotel options
AddressLabel = Label(HotelDescriptionFrame, text="",font=("Arial", 15))
AddressLabel.grid(row=1, column=0, sticky=NW)

# heading for reviews
ReviewListHeaderText = Label(HotelReviewFrame, text="Reviews", font=("Arial", 15))
ReviewListHeaderText.grid(row=0, column=0, sticky=NW)

#Address label in display hotel options
FacilitiesLabel = Label(HotelDescriptionFrame, text="",font=("Arial", 15))
FacilitiesLabel.grid(row=2, column=0, sticky=NW)

#average star review label in display hotel options
AverageScoreLabel = Label(HotelDescriptionFrame, text="",font=("Arial", 15))
AverageScoreLabel.grid(row=3, column=0, sticky=NW)

#No results label in main menu
Emptylabel = Label(MainMenuFrame,text="No Results", font=("Arial", 20), width=37)

#filter options
FilterLabel = Label(FilterFrame, text="Filters", font=("Arial", 20))
#filter variables
restaurant=StringVar()
jacuzzi=StringVar()
pool=StringVar()
gym=StringVar()
spa=StringVar()

#Label for ameneties and checkboxes for ameneties filter
AmenitiesLabel = Label(FilterFrame, text="Amenities", font=("Arial", 15))
RestaurantFilter = Checkbutton(FilterFrame, text="Restaurant", variable=restaurant, onvalue="restaurant", offvalue= "na", command=FilterAndSortHotelDetails)
JacuzziFilter = Checkbutton(FilterFrame, text="Jacuzzi", variable=jacuzzi, onvalue="jacuzzi", offvalue= "na", command=FilterAndSortHotelDetails)
PoolFilter = Checkbutton(FilterFrame, text="Pool", variable=pool, onvalue="pool", offvalue= "na", command=FilterAndSortHotelDetails)
GymFilter = Checkbutton(FilterFrame, text="Gym", variable=gym, onvalue="gym", offvalue= "na", command=FilterAndSortHotelDetails)
SpaFilter = Checkbutton(FilterFrame, text="Spa", variable=spa, onvalue="spa", offvalue= "na", command=FilterAndSortHotelDetails)
#deselect checkboxes, string var makes it select by default
RestaurantFilter.deselect()
JacuzziFilter.deselect()
PoolFilter.deselect()
GymFilter.deselect()
SpaFilter.deselect()

#Label for ratings and checkboxes for rating filter
RatingLabel = Label(FilterFrame, text="Rating", font=("Arial", 15))
onestar=IntVar()
twostar=IntVar()
threestar=IntVar()
fourstar=IntVar()
fivestar=IntVar()

OneStarFilter = Checkbutton(FilterFrame, text="1 Star", variable=onestar, onvalue=1, offvalue= 0, command=FilterAndSortHotelDetails)
TwoStarFilter = Checkbutton(FilterFrame, text="2 Stars", variable=twostar, onvalue=2, offvalue= 0, command=FilterAndSortHotelDetails)
ThreeStarFilter = Checkbutton(FilterFrame, text="3 Stars", variable=threestar, onvalue=3, offvalue= 0, command=FilterAndSortHotelDetails)
FourStarFilter = Checkbutton(FilterFrame, text="4 Stars", variable=fourstar, onvalue=4, offvalue= 0, command=FilterAndSortHotelDetails)
FiveStarFilter = Checkbutton(FilterFrame, text="5 Stars", variable=fivestar, onvalue=5, offvalue= 0, command=FilterAndSortHotelDetails)

FilterLabel.grid(row=0, column=0, sticky=W)
AmenitiesLabel.grid(row=1, column=0, sticky=W)
RestaurantFilter.grid(row=2, column=0, sticky=W)
JacuzziFilter.grid(row=3, column=0, sticky=W)
PoolFilter.grid(row=4, column=0, sticky=W)
GymFilter.grid(row=5, column=0, sticky=W)
PoolFilter.grid(row=6, column=0, sticky=W)
SpaFilter.grid(row=7, column=0, sticky=W)
RatingLabel.grid(row=8, column=0, sticky=W)
OneStarFilter.grid(row=9, column=0, sticky=W)
TwoStarFilter.grid(row=10, column=0, sticky=W)
ThreeStarFilter.grid(row=11, column=0, sticky=W)
FourStarFilter.grid(row=12, column=0, sticky=W)
FiveStarFilter.grid(row=13, column=0, sticky=W)

# set default value of sort
SortVariable = StringVar()
SortVariable.set(MainMenuSortOptions[0])
#add frame for sort widgets
SortFrame = Frame(master=MainMenuFrame, padx=10, pady=5)
SortFrame.grid(row=0, column=0, sticky=NW)
SortLabel = Label(SortFrame, text="Sort by:", font=("Arial", 14))
SortLabel.grid(row=0, column=0, sticky=NW)
#create sort dropdown
SortDropdown = OptionMenu(SortFrame, SortVariable, *MainMenuSortOptions, command=FilterAndSortHotelDetails)
SortDropdown.grid(row=0, column=1, sticky=NW)
add_hotel = Button(MainMenuFrame, text = "Add Hotel", command= open_popup)
add_hotel.grid(row=0, column=0, sticky=E, padx=10)

#set default value for bookmark widget
BookmarkNameVariable = StringVar()
BookmarkNameVariable.set("Bookmarks")
if (len(BookmarkedHotelsNameList) == 0): #give default list of bookmarks no bookmarks if no bookmarked hotels
    BookmarkedHotelsNameList.append("No Bookmarks")
# create bookmark dropdown
BookmarkDropdown = OptionMenu(ContentFrame, BookmarkNameVariable, *BookmarkedHotelsNameList, command=SelectFromBookmark)
BookmarkDropdown.grid(row=0, column=0, sticky=W, padx=40)


#bookmarked checkbutton in display hotel details
BookmarkedVariable = BooleanVar()
BookmarkedButton = Checkbutton(HotelNameFrame, text="Bookmarked", variable=BookmarkedVariable, onvalue=1, offvalue= 0, command=ToggleBookmark)
BookmarkedButton.grid(row=0, column=1, sticky=W)

#Show analysis 
ShowAnalysisButton = Button(HotelNameFrame, text = "Show analysis", command=showAnalysis)
ShowAnalysisButton.grid(row=0, column=2)

#Show keywords
ShowEmotionButton = Button(HotelNameFrame, text = "Show keywords", command=showEmotions)
ShowEmotionButton.grid(row=0, column=3)

#add frame for sort widgets
ReviewFilterFrame = Frame(master=HotelReviewFrame, pady=5)
ReviewFilterFrame.grid(row=1, column=0, sticky=NSEW)
ReviewFilterLabel = Label(ReviewFilterFrame, text="Filter by:", font=("Arial", 10))
ReviewFilterLabel.grid(row=0, column=0, sticky=NW)
#create sort dropdown
ReviewFilterVariable = StringVar()
ReviewFilterVariable.set(ReviewFilterOptions[0])
FilterReviewDropdown = OptionMenu(ReviewFilterFrame, ReviewFilterVariable, *ReviewFilterOptions, command=FilterReviews)
FilterReviewDropdown.grid(row=0, column=1, sticky=NW)


#sort and filter main menu based on default values
FilterAndSortHotelDetails(SortVariable)
#show main menu widgets
DisplayMainMenu()
window.mainloop()
