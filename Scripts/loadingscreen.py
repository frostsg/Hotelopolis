from tkinter import *
import math
import pandas
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os.path
from Scripts.filtering import *

from PIL import ImageTk, Image
from Scripts.review_analysis import *

# JFStart
import os
import os.path
import time
import PIL as p
import PIL.ImageTk as ptk
import bs4
import requests
from Scripts.webscraper import *
from PIL import Image
# google
from selenium import webdriver

from Scripts.webscraper import urlchecker
from selenium.webdriver.chrome.options import Options


#loading screen 
import tkinter as tk
from time import sleep


import tkinter
from tkinter import *
from PIL import Image, ImageTk

root = Tk()


#end

from tkinter import *
from PIL import Image, ImageTk


def task():
    # The window will stay open until this function call ends.
    sleep(2) # Replace this with the code you want to run
    root.destroy()

img = ImageTk.PhotoImage(Image.open("GdTTaIrf_400x400.png"))
panel = Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
root.geometry("400x400+520+150")
root.resizable(width=True, height=True)


root.after(2000, task)
root.mainloop()

print("Main loop is now over and we can do other stuff.")