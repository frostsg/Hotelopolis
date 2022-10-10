
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import functools
#reference:https://towardsdatascience.com/machine-learning-text-processing-1d5a2d638958

# This feature is a work in progress 

review1=""" 
The hotel is just one of many that are on this new trend of firmer pillows and mattresses. This is the third hotel I have stayed in the last few months that have had firmer vs softer mattresses in their rooms. Aside from the bed The room was well appointed, comfortable and really The bonus Those super plushy and comfy robes in the closet. I miss a good hotel robe and this one had one!! Another little thing 
I loved was the spa water and coffee service in the lobby. High quality coffee and the New York Times Count me in! The maid service was friendly, attentive, and I even got a little note. Would totally stay again.
excellent location near convention center. friendly, willing staff. not a true luxury hotel in terms of the room I received, but a comfortable clean room, I didn't really need any more than that. After all you're here to visit San Francisco, not the hotel.
Hotel Zelos was a great place to stay in San Francisco. The staff is definitely the highlight of the hotel. The hotel itself is great: clean, well decorated, etc, but the people who work there were very helpful and friendly. The location is great being right next to the Powell BART station but the neighborhood is under construction. This obviously isn't the fault of the hotel and won't impact your stay. We couldn't hear any of the construction, but it makes it a little more difficult to get around. Overall, I definitely recommend Hotel Zelos!
Pros: the location is awesome, the room size is great, the bathroom is nice also with a nice tub. Bad: the style and furniture starts to get really old, no breakfast despite the high price, the price is high, nothing exeptionnal... We were 4 people and so 4 reservations. Unfortunately one was missing. It was 1am so very bad surprise.... More
""" # four reviews concantenated

review="""
Pleasant 10 min walk along the sea front to the Water Bus. restaurants etc. Hotel was comfortable breakfast was good - quite a variety. Room aircon didn't work very well. Take mosquito repelant!
Really lovely hotel. Stayed on the very top floor and were surprised by a Jacuzzi bath we didn't know we were getting! Staff were friendly and helpful and the included breakfast was great! Great location and great value for money. Didn't want to leave!
We stayed here for four nights in October. The hotel staff were welcoming, friendly and helpful. Assisted in booking tickets for the opera. The rooms were clean and comfortable- good shower, light and airy rooms with windows you could open wide. Beds were comfortable. Plenty of choice for breakfast.Spa at hotel nearby which we used while we were there.
We loved staying on the island of Lido! You need to take a water is from Venice to get there. From the train station, a boat ride takes 45 minutes but has beautiful views along the way. Hotel is an EASY walk from the boat dock. The room was very clean and the breakfast was plentiful. We would definitely recommend this hotel!
disgusting food. It had a bad experience in the restaurant. They very very expensive too. I will never return
"""

review=review.lower() # change case to lower 
facilities=['restaurant','gym', 'jacuzzi','sauna','hot','tub','food','pool','spa','breakfast','dinner','lunch'] # reference list of facilites, Used for string matching
tokens=word_tokenize(review) # nlp, split para or sentence to smaller units (strings) into a list
stop_words = set(stopwords.words('english')) # remove unimpt words e.g 'a, the, for, to'
tokens = [word for word in tokens if not word in stop_words] # remove unimpt words e.g 'a, the, for, to'
tokens=[*set(tokens)] # remove duplicate words

print("Hotel Facilities are: ",(list(set(tokens).intersection(facilities)))) # display common words from 2 lists - tokens and facilties

neg_emotions=['unaffordable','disgusting','bad','poor','expensive','dirty','sad','uncomfortable']
pos_emotions=['affordable','good','comfortable','nice','beautiful','luxury','happy','joy','lovely','friendly','helpful','pleasant','awesome']
#print("\nGood aspects: ",(list(set(tokens).intersection(pos_emotions))))
aspects=(list(set(tokens).intersection(pos_emotions+neg_emotions)))
frequency_dist = nltk.FreqDist(aspects)
wordcloud = WordCloud().generate_from_frequencies(frequency_dist)
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


"""
#Display word cloud

frequency_dist = nltk.FreqDist(tokens)
wordcloud = WordCloud().generate_from_frequencies(frequency_dist)
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

"""
"""
work in progress 7 oct 2022
  #restaurant=['food','coffee','tea','breakfast','lunch','dinner']
  
  """