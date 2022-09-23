import tkinter as tk
import pandas as pd
import csv

##########Initialise values############
window = tk.Tk()
data = pd.read_csv("../Datafiniti_Hotel_Reviews.csv")
window.geometry("500x500")

#reviews text manager
ReviewsTextList=[]
#review score /5 manager
ReviewsScoreList=[]

#variable for dropdown box option
ChosenHotel = tk.StringVar()
ChosenHotel.set("Choose Hotel")

#dropdown box options
HotelOptions=[
    'Aloft Arundel Mills',
    'Econolodge',
    'Hotel Zelos',
    'Fairmont Grand Del Mar',
    'Best Western at OHare',
    'Virgin Hotels Chicago'
]

#################functions#####################
#clear current hotel details and formatting
def ClearHotelDetails():
    HotelNameLabel.grid_forget()
    AddressLabel.grid_forget()
    AverageScoreLabel.grid_forget()
    ReviewCanvas.pack_forget()
    VScrollbar.pack_forget()
    HScrollbar.pack_forget()
    for Review in ReviewsTextList:
        Review.destroy()
    for Review in ReviewsScoreList:
        Review.destroy()

    ReviewsTextList.clear()
    ReviewsScoreList.clear()

#logic for UI display, it clears details and reformats it for the new hotel
def DisplayHotelDetails():
    if ChosenHotel.get() == "Choose Hotel":
        return
    ClearHotelDetails()

    HotelNameLabel.config(text=ChosenHotel.get())
    HotelNameLabel.grid(row=2, column=0)

    Address = data.loc[data.name == ChosenHotel.get(), 'address']
    AddressLabel.config(text=("Address:", Address.iat[0]))
    AddressLabel.grid(row=3, column=0)

    ReviewsList = list(data.loc[data.name == ChosenHotel.get(), 'reviews.text'])
    #star reviews
    ReviewsRating = list(data.loc[data.name == ChosenHotel.get(), 'reviews.rating'])

    #average rating
    TotalScore = 0
    for rating in ReviewsRating:
        TotalScore += int(rating)

    AverageScore = TotalScore/len(ReviewsRating)
    AverageScoreLabel.config(text= "Score: %0.2f"%AverageScore+ "/5")
    AverageScoreLabel.grid(row=4, column=0)

    #table heading
    ReviewListHeaderStars = tk.Label(InternalReviewFrame, text="Rating")
    ReviewListHeaderText = tk.Label(InternalReviewFrame, text="Reviews")
    ReviewListHeaderStars.grid(row=0,column=0, sticky="w")
    ReviewListHeaderText.grid(row=0, column=1, sticky="w")
    ReviewsTextList.append(ReviewListHeaderStars)
    ReviewsTextList.append(ReviewListHeaderText)

    #display reviews score/5
    for i, k in enumerate(ReviewsRating):
        ReviewsScoreText = tk.Label(InternalReviewFrame, text=ReviewsRating[i])
        ReviewsScoreText.grid(row=i + 1, column=0, sticky="w")
        ReviewsScoreList.append(ReviewsScoreText)

        # review text
    for i, k in enumerate(ReviewsList):
        ReviewsText = tk.Label(InternalReviewFrame, text=ReviewsList[i], justify=tk.LEFT)
        ReviewsText.grid(row=i + 1, column=1, sticky="w")
        ReviewsTextList.append(ReviewsText)


    #scrollbar
    #update size of content for scrollbar
    ReviewCanvas.update_idletasks()
    ReviewCanvas.config(scrollregion=ReviewCanvas.bbox("all"))
    #reset scrollbar position to start
    ReviewCanvas.xview_moveto(0)
    ReviewCanvas.yview_moveto(0)
    #pack scrollbar and canvas
    HScrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    VScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    ReviewCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


##########UI LAYOUT##########
#frame for entire window
WindowFrame = tk.Frame(master=window)
WindowFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
#expand widget with window size
WindowFrame.columnconfigure(0, weight=1)
WindowFrame.rowconfigure(0, weight=1)

#search and detail frame
SearchAndDetailFrame = tk.Frame(master=WindowFrame)
SearchAndDetailFrame.grid(row=0, column=0, sticky=tk.NS)

#dropdown box
Dropdown = tk.OptionMenu(SearchAndDetailFrame, ChosenHotel , *HotelOptions)
Dropdown.grid(row=0,column=0, sticky="N")

#Search button
Button = tk.Button(SearchAndDetailFrame, text="GO", command=DisplayHotelDetails)
Button.grid(row=1, column=0, sticky="N")

#Hotel name label
HotelNameLabel = tk.Label(SearchAndDetailFrame, text="Welcome", font=("Arial", 25))

#Address label
AddressLabel = tk.Label(SearchAndDetailFrame, text="")

#average star review label
AverageScoreLabel = tk.Label(SearchAndDetailFrame, text="")

#frame for review canvas
ReviewFrame = tk.Frame(master=WindowFrame)
ReviewFrame.grid(row=1,column=0, sticky=tk.NSEW)

#canvas for reviews
ReviewCanvas = tk.Canvas(master=ReviewFrame)
VScrollbar = tk.Scrollbar(master=ReviewFrame, orient=tk.VERTICAL)
HScrollbar = tk.Scrollbar(master=ReviewFrame, orient=tk.HORIZONTAL)

#Frame for reviews
InternalReviewFrame= tk.Frame(ReviewCanvas)
ReviewCanvas.create_window((0,0), window=InternalReviewFrame, anchor=tk.NW)
ReviewCanvas.configure(xscrollcommand=HScrollbar.set, yscrollcommand=VScrollbar.set)
HScrollbar.config(command=ReviewCanvas.xview)
VScrollbar.config(command=ReviewCanvas.yview)

window.mainloop()