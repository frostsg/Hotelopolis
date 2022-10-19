"""
This program filter amenities in a hotel by identify keywords related to amenities in the reviews - ragnar170

"""
# code reference for nlp :https://towardsdatascience.com/machine-learning-text-processing-1d5a2d638958

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import functools



# reference lists
restaurant_list = ['Restaurant', 'Food', 'Coffee', 'Tea', 'Breakfast', 'Lunch', 'Dinner', 'Buffet']  # ref list for restaurant filter
pool_list = ['Pool', 'Swimming']
jacuzzi_list = ['Jacuzzi', 'Hot tub', 'Tub']  # ref list for pool filter
gym_list = ['Gym', 'workout', 'exercise', 'treadmill', 'dumbbells']  # ref list for gym filter
spa_list = ['Spa', 'health', 'sauna', 'massage']  # ref list for spa filter
facility_options = {1: restaurant_list, 2: pool_list, 3: jacuzzi_list,  4: gym_list, 5: spa_list}
neg_emotions = ['worst','noisy','unaffordable', 'disgusting', 'poor', 'expensive', 'dirty', 'uncomfortable', 'rude','hassle', 'horrible', 'noisy', 'broken','small','smelly','old','poor','basic']
pos_emotions = ['great','relaxing','perfect','high quality','wonderful','affordable','clean', 'comfort', 'comfortable', 'beautiful', 'luxury', 'happy', 'joy', 'lovely','friendly', 'helpful', 'pleasant', 'awesome']
other_facilities=['staff','location','wifi','beds','rooms','bathroom', 'kitchen']
pos_aspect_list=restaurant_list+pool_list+jacuzzi_list+gym_list+spa_list+pos_emotions+other_facilities
neg_aspect_list=restaurant_list+pool_list+jacuzzi_list+gym_list+spa_list+neg_emotions+other_facilities
# check if 2 lists have common item or not
def common_item(x, y):
    res=False
    for i in x:
        for j in y:
            if i==j:
                res=True
                #answer="there is a common item"
                return res
    return res

def remove_no(list1):
    # to avoid including "no pool" in the filter, this function removes "no" and the word after it
    for i in range(0, len(list1) - 1):
        while(list1[i]=='no'):
            list1.pop(i)
            list1.pop(i+1)
            continue
        else:
            break
    return(list1)

def tokenize(reviewlist):
    # breaks down significant words in the review to tokens using nlp
    review = reviewlist.lower()  # change case to lower
    tokens = word_tokenize(review)  # nlp, split para or sentence to smaller units (strings) into a list
    remove_no(tokens) # to avoid discrepancy like "no pool", "no gym"
    stop_words = set(stopwords.words('english'))  # set of stopwords (approx. 40) in english language
    tokens = [word for word in tokens if not word in stop_words]  # remove unimpt words e.g 'a, the, for, to'
    tokens = [*set(tokens)]  # remove duplicate words
    return tokens

def facility_check(reviewlist):
    facility_list=[]
    #global review, restaurant_list, gym_list, spa_list, pool_list, facility_options

    # NLP to convert review into tokens
    tokens=tokenize(reviewlist)

    # user options 1 for restaurant, 2 - pool, 3 - Gym, 4 - Sauna
    counter = 0
    # if user input is 1, then it compares review words with strings in restaurant list "1:restaurant_list"
    for key in facility_options:  # if key of the ref list matches with user option
        counter += 1
        if key == counter and counter <= 5:
            fac_list = ([x.lower() for x in facility_options[counter]])  # converts strings in list to lowercase
            # expected result : True or False (true - means the facility is found in the review)
            if (common_item(tokens, fac_list)) is True:
                facility_list.append(fac_list[0])  # append the facility to the prev created empty list
            else:
                continue
        else:
            break
    return facility_list



# display common words from 2 sets/lists - tokens (review) and facilties
# print("Hotel Facilities are: ",(list(set(tokens).intersection(facilities))))
# showing good aspects from review
# print("\nGood aspects: ",(list(set(tokens).intersection(pos_emotions))))

