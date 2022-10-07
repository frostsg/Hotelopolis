from tkinter import *
import pandas as pd
import csv
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

##########Initialise values############
window = Tk()
data = pd.read_csv("../../../AssignmentTest/venv/Datafiniti_Hotel_Reviews.csv")
window.geometry("900x600")
window.option_add("*Background", "white")

senti = SentimentIntensityAnalyzer()

#reviews text manager
ReviewsTextList=[]
#review score /5 manager
ReviewsScoreList=[]
#hotel menu list
HotelMenuList=[]
#Hotels List
HotelsList =[]
#Recommended Hotels List
RecommendedHotelsList =[]

class Hotel:
    def __init__(self, name, address, scoreslist, reviewslist):
        self.Name = name
        self.Address = address
        self.ScoresList = scoreslist
        self.ReviewsList = reviewslist
        TotalScore = 0
        for rating in ReviewsRating:
            TotalScore += int(rating)

        self.AverageScore = TotalScore / len(ReviewsRating)

        analysis ={}
        analysis["Positive"] = [senti.polarity_scores(i)["pos"] for i in self.ReviewsList]
        analysis["Negative"] = [senti.polarity_scores(i)["neg"] for i in self.ReviewsList]
        self.Sentiments = analysis

#dropdown box options
HotelOptions=[
    'Aloft Arundel Mills',
    'Econolodge',
    'Hotel Zelos',
    'Fairmont Grand Del Mar',
    'Best Western at OHare',
    'Virgin Hotels Chicago',
    'Rancho Valencia Resort Spa'
]

SortOptions = [
    'Alphabetical A-Z',
    'Alphabetical Z-A',
    'Rating (High to Low)',
    'Rating (Low to High)'
    ]


#################functions#####################
#clear current hotel details and formatting
def ClearMainMenu():
    MainMenuFrame.grid_forget()
    FilterFrame.grid_forget()

def ClearHotelDetails():
    RecommendationFrame.grid_forget()
    HotelDetailsFrame.grid_forget()
    MenuButton.grid_forget()
    for Review in ReviewsTextList:
        Review.destroy()
    for Review in ReviewsScoreList:
        Review.destroy()

    ReviewsTextList.clear()
    ReviewsScoreList.clear()

def FilterAndSortHotelDetails(sortoption = None):
    for HotelButton in HotelMenuList:
        HotelButton.destroy()

    HotelMenuList.clear()

    if(SortVariable.get() == 'Alphabetical A-Z'):
        SortedList = sorted(HotelsList, key= lambda x:x.Name)
    elif(SortVariable.get() == 'Alphabetical Z-A'):
        SortedList = sorted(HotelsList, key= lambda x:x.Name, reverse=True)
    elif (SortVariable.get() == 'Rating (High to Low)'):
        SortedList = sorted(HotelsList, key=lambda x: x.AverageScore, reverse=True)
    elif (SortVariable.get() == 'Rating (Low to High)'):
        SortedList = sorted(HotelsList, key=lambda x: x.AverageScore)


    if(var1.get() == 0 and var2.get() == 0 and var3.get() == 0 and var4.get() == 0 and var5.get() == 0):
        for index, hotel in enumerate(SortedList):
            HotelMenuButton = Button(MainMenuFrame, text=hotel.Name + "\n"+hotel.Address + "\n Average Score: %0.2f" % hotel.AverageScore,
                                     command=lambda hotel=hotel: DisplayHotelDetails(hotel), width=80, height=6, font=("Arial", 10), relief=GROOVE)
            HotelMenuButton.grid(row=index+1, column=0, sticky=N, pady=10, padx=10)
            HotelMenuList.append(HotelMenuButton)
    else:
        for index, hotel in enumerate(SortedList):
            if(int(hotel.AverageScore) == var1.get() or int(hotel.AverageScore) == var2.get() or int(hotel.AverageScore) == var3.get() or int(hotel.AverageScore) == var4.get() or int(hotel.AverageScore) == var5.get()):
                HotelMenuButton = Button(MainMenuFrame, text=hotel.Name + "\n"+hotel.Address +"\n Average Score: %0.2f" % hotel.AverageScore, command=lambda hotel=hotel: DisplayHotelDetails(hotel), width=80, height=6, font=("Arial", 10), relief=GROOVE)
                HotelMenuButton.grid(row=index + 2, column=0, sticky=N, pady=10, padx=10)
                HotelMenuList.append(HotelMenuButton)

    UpdateScrollbar()

def UpdateRecommendations(hotel):
    for HotelButton in RecommendedHotelsList:
        HotelButton.destroy()
    for index, otherhotel in enumerate(HotelsList):
        if (round(otherhotel.AverageScore) >= hotel.AverageScore and otherhotel.Name != hotel.Name):
            RecoHotelMenuButton = Button(RecommendationFrame, text=otherhotel.Name + "\n Average Score: %0.2f" % otherhotel.AverageScore,
                                     command=lambda otherhotel=otherhotel: DisplayHotelDetails(otherhotel), width=20, height=4, font=("Arial", 10), relief=GROOVE)
            RecoHotelMenuButton.grid(row=index+1, column=0, sticky=N, pady=10, padx= 10)
            RecommendedHotelsList.append(RecoHotelMenuButton)

def UpdateScrollbar():
    # scrollbar
    # update size of content for scrollbar
    MainCanvas.update_idletasks()
    MainCanvas.config(scrollregion=MainCanvas.bbox("all"))
    # reset scrollbar position to start
    MainCanvas.xview_moveto(0)
    MainCanvas.yview_moveto(0)

def DisplayMainMenu():
    ClearHotelDetails()
    FilterFrame.grid(row=1, column=0, sticky=N, padx=40)
    MainMenuFrame.grid(row=1, column=1, sticky=N)
    UpdateScrollbar()

#logic for UI display, it clears details and reformats it for the new hotel
def DisplayHotelDetails(hotel):
    ClearHotelDetails()
    ClearMainMenu()

    HotelNameLabel.config(text=hotel.Name)
    HotelNameLabel.grid(row=0, column=0, sticky=NW)

    AddressLabel.config(text=("Address: " + hotel.Address))
    AddressLabel.grid(row=1, column=0, sticky=NW)

    AverageScoreLabel.config(text= "Score: %0.2f"%hotel.AverageScore+ "/5")
    AverageScoreLabel.grid(row=2, column=0, sticky=NW)

    #table heading
    ReviewListHeaderStars = Label(HotelReviewFrame, text="Rating")
    ReviewListHeaderText = Label(HotelReviewFrame, text="Reviews")
    ReviewListHeaderStars.grid(row=3,column=0, sticky=NW)
    ReviewListHeaderText.grid(row=3, column=1, sticky=NW)
    ReviewsTextList.append(ReviewListHeaderStars)
    ReviewsTextList.append(ReviewListHeaderText)

    #display reviews score/5
    for index, score in enumerate(hotel.ScoresList):
        ReviewsScoreText = Label(HotelReviewFrame, text=score)
        ReviewsScoreText.grid(row=index +4, column=0, sticky=NW)
        ReviewsScoreList.append(ReviewsScoreText)

        # review text
    for index, review in enumerate(hotel.ReviewsList):
        ReviewsText = Label(HotelReviewFrame, text=review, justify=LEFT)
        ReviewsText.grid(row=index + 4, column=1, sticky=NW)
        ReviewsTextList.append(ReviewsText)


        #temporary
    SentimentalScoresLabel = Label(HotelReviewFrame, text="Scores(Pos, Neg, Neu)")
    SentimentalScoresLabel.grid(row=3, column=2)
        # sentimental analysis data
    for index, sentimentalscore in enumerate(hotel.Sentiments["Positive"]):
        SentimentText = Label(HotelReviewFrame, text=sentimentalscore, justify=LEFT)
        SentimentText.grid(row=index + 4, column=2, sticky=W)
        ReviewsTextList.append(SentimentText)

    for index, sentimentalscore in enumerate(hotel.Sentiments["Negative"]):
        SentimentText = Label(HotelReviewFrame, text=sentimentalscore, justify=LEFT)
        SentimentText.grid(row=index + 4, column=3, sticky=W)
        ReviewsTextList.append(SentimentText)

    UpdateRecommendations(hotel)
    RecommendationFrame.grid(row=1, column=0, padx=40, sticky=N)
    HotelDetailsFrame.grid(row=1, column=1, sticky=N)
    MenuButton.grid(row=10, column=0, padx=10, pady=10)
    UpdateScrollbar()


#####INITIALISE HOTELS#####
for i in HotelOptions:
    #create hotels
    ReviewsList = list(data.loc[data.name == i, 'reviews.text'])
    ReviewsRating = list(data.loc[data.name == i, 'reviews.rating'])
    AddressList =  data.loc[data.name == i, 'address']
    Address = AddressList.iat[0]
    HotelObject = Hotel(i, Address, ReviewsRating, ReviewsList)
    HotelsList.append(HotelObject)


##########UI LAYOUT##########
#frame for entire window
MainFrame = Frame(master=window)
MainFrame.pack(side=LEFT, fill=BOTH, expand=1)

#canvas for reviews
MainCanvas = Canvas(master=MainFrame)
VScrollbar = Scrollbar(master=MainFrame, orient=VERTICAL, command=MainCanvas.yview)
HScrollbar = Scrollbar(master=MainFrame, orient=HORIZONTAL, command=MainCanvas.xview)

VScrollbar.pack(side=RIGHT, fill=Y)
HScrollbar.pack(side=BOTTOM, fill=X)

#Frame for reviews
ContentFrame= Frame(MainCanvas)
MainCanvas.create_window((0,0), window=ContentFrame, anchor=NW)
MainCanvas.configure(xscrollcommand=HScrollbar.set, yscrollcommand=VScrollbar.set)
MainCanvas.pack(side=LEFT, fill=BOTH, expand=1)

#Title Frame
TitleFrame =  Frame(master=ContentFrame)
TitleFrame.grid(row=0, column=1)

#Filter Frame
FilterFrame = Frame(master=ContentFrame, highlightbackground="black", highlightthickness=1, padx=10, pady=5)

#Recommendation Frame
RecommendationFrame = Frame(master=ContentFrame, highlightbackground="black", highlightthickness=1,padx=10, pady=5)

#Frame for hotel buttons, hotel info
MainMenuFrame = Frame(master=ContentFrame)

#Frame for Hotels and reviews
HotelDetailsFrame = Frame(master=ContentFrame, highlightbackground="black", highlightthickness=1,padx=10, pady=5)

HotelDescriptionFrame = Frame(master=HotelDetailsFrame)
HotelDescriptionFrame.grid(row=0, column=0, sticky=NW)
HotelReviewFrame =  Frame(master=HotelDetailsFrame)
HotelReviewFrame.grid(row=1, column=0, sticky=NW)


#Title
AppTitleLabel = Label(TitleFrame, text="HOTELOPOLIS", font=("Arial", 40), anchor=CENTER)
AppTitleLabel.grid(row=0, column=0)

#filter options
FilterLabel = Label(FilterFrame, text="Filters", font=("Arial", 20))
AmenitiesLabel = Label(FilterFrame, text="Amenities", font=("Arial", 15))
PoolFilter = Checkbutton(FilterFrame, text="Pool", variable=0)

#Recommendation Label
RecommendationLabel = Label(RecommendationFrame, text="You may also like:")
RecommendationLabel.grid(row=0, column=0)

#Menu Button
MenuButton = Button(RecommendationFrame, text="Back To Menu", command=DisplayMainMenu,font=("Arial", 10), relief=GROOVE)

#Hotel name label
HotelNameLabel = Label(HotelDescriptionFrame, font=("Arial", 30))

#Address label
AddressLabel = Label(HotelDescriptionFrame, text="",font=("Arial", 15))

#average star review label
AverageScoreLabel = Label(HotelDescriptionFrame, text="",font=("Arial", 15))

RatingLabel = Label(FilterFrame, text="Rating", font=("Arial", 15))
var1=IntVar()
var2=IntVar()
var3=IntVar()
var4=IntVar()
var5=IntVar()
OneStarFilter = Checkbutton(FilterFrame, text="1 Star", variable=var1, onvalue=1, offvalue= 0, command=FilterAndSortHotelDetails)
TwoStarFilter = Checkbutton(FilterFrame, text="2 Stars", variable=var2, onvalue=2, offvalue= 0, command=FilterAndSortHotelDetails)
ThreeStarFilter = Checkbutton(FilterFrame, text="3 Stars", variable=var3, onvalue=3, offvalue= 0, command=FilterAndSortHotelDetails)
FourStarFilter = Checkbutton(FilterFrame, text="4 Stars", variable=var4, onvalue=4, offvalue= 0, command=FilterAndSortHotelDetails)
FiveStarFilter = Checkbutton(FilterFrame, text="5 Stars", variable=var5, onvalue=5, offvalue= 0, command=FilterAndSortHotelDetails)

FilterLabel.grid(row=0, column=0, sticky=W)
AmenitiesLabel.grid(row=1, column=0, sticky=W)
PoolFilter.grid(row=2, column=0, sticky=W)
RatingLabel.grid(row=4, column=0, sticky=W)
OneStarFilter.grid(row=5, column=0, sticky=W)
TwoStarFilter.grid(row=6, column=0, sticky=W)
ThreeStarFilter.grid(row=7, column=0, sticky=W)
FourStarFilter.grid(row=8, column=0, sticky=W)
FiveStarFilter.grid(row=9, column=0, sticky=W)

SortVariable = StringVar()
SortVariable.set(SortOptions[0]) # default value

SortFrame = Frame(master=MainMenuFrame, padx=10, pady=5)
SortFrame.grid(row=0, column=0, sticky=NW)
SortLabel = Label(SortFrame, text="Sort by:", font=("Arial", 14))
SortLabel.grid(row=0, column=0, sticky=NW)
SortDropdown = OptionMenu(SortFrame, SortVariable, *SortOptions, command=FilterAndSortHotelDetails)
SortDropdown.grid(row=0, column=1, sticky=NW)

FilterAndSortHotelDetails(SortVariable)
DisplayMainMenu()
window.mainloop()
