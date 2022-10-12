
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from filtering import *

# please remove this comment and below "doc" after integration
doc="""
We had a wonderful, relaxing time. The staff were completely attentive and accommodating. We had a corner king room with a kitchen, two patios and a deluxe bathroom. You had to drive into town but they said that Uber is available if you need it. This was our first visit to Palm Springs and hopefully not our last! It really... More
We were in Palm Springs on the day the temperature was 123 degrees! Despite that, we had a wonderful stay because of the Little Paradise hotel. The staff were friendly and accommodating, and all of the little complimentary touches were so nice, like a bottle of wine for us in the fridge, sun care products near the pool, and a... More
We arrived in Palm Springs not sure what to expect....it's a quiet kinda place in 'low season'....we drove down what appeared to be a residential street...parked up at a wooden gate and weren't sure what to expect. What awaited took us back in amazement...the room is spacious with an air of decadence...the welcome wine and comprehensive breakfast was more than... More
This place really is a little paradise!! A beautiful boutique style hotel with EVERYTHING meticulously thought out to make our vacation perfect. Saltwater pool, fresh fruit, BEST showerhead I've ever experienced, I can go on and on. The bed was so comfortable and we slept like babies. Victor did a wonderful job and Judy was just lovely and personable!
Spent 3 nights at Little Paradise boutique hotel on a mother-daughter trip. Wonderful and relaxing experience. Clean and newly redone rooms that are well equipped and spacious. Perfect location off the main street in a quiet neighborhood that is close to downtown Palm Springs. The pool area has a nice gas fire pit area and lots of comfy chaise lounges... More
This little hotel surpassed all my expectations. The rooms are well equiped with a little kitchenette, fridge was filled with croissants, 3 bottles of water, soda and much more. The room was very clean and the bathroom was equiped with a top notch shower. I would definately recommend this place to anyone visiting or passing trough Palm Springs. The reception... More
If you want peaceful and relaxing look no further. Although set up like a single floor motel it is hardly anything but. The rooms are very nice with a full kitchen. They provide some breakfast items, snacks and bottles of spring water. You can bring in anything you like to enjoy at the pool or in your room. By the... More
All the reviews are great and agree on this fine little place. I'd also like to add the wonderful service you will find here with Victor and staff who seem to want to do anything and everything to make you happy. The king beds here are just amazing. We seldom run into beds this comfy. The room has a large... More
We went for a relaxing weekend as an offshoot of a family visit. This was a great place to go with a nice room and a view of the mountains from just outside. The ONLY thing we didn't like was that the sun dropped below the mountains too early and the temperature dropped along with it. Maybe you can fix... More
We were on a business trip to Anaheim and, afterwards, drove to Palm Springs for a relaxing weekend. It turned out that this hotel was the perfect place! We arrived late and were pleasantly surprised upon checking in to see that, not only were the accommodations incredibly thoughtful and comfortable, but the refrigerator came stocked with croissants, bagels, cream cheese,... More
Victor and Judy were truly accommodating hosts, especially when we had to cut our stay short due to illness. Everything that has been written by other reviewers was spot on. It is more like a small inn or bed breakfast (with the breakfast left in the fridge in your room) than a hotel. There are eight guest rooms around... More
If you want to relax, want a quiet atmosphere, cozy setting.. this is the place. It is definitely a smaller, boutique-type hotel and it feels that way. So that's good for some and maybe not as much for others. The room is great, very pretty. Very impressive large, new Curved HD TV. So that's nice! The small kitchen is also... More
Stayed 5 nights and it was delightful. Lovely comfortable,well lit, great shower and bathroom,kitchen with microwave,fridge etc and very functional room. Ten hotels on this trip but this one seems to have thought of everything. Peaceful yet near the main streets with lovely shopping, art and some great restaurants. Good local transport but downtown is walkable but a bit over... More
New everything would be great from the moment we came through the gate. Nine excellent, high quality rooms each with a small kitchen/diner and terrific shower room including twin wash basins. Each room faces onto the pool with plenty of sun loungers, towels, shaded areas and comfortable seating. Rooms furnished to extremely high standard and beds have the finest linen... More
Spend four days there and would have prolonged our stay if they only had a room available. Welcoming host, all rooms around the patio / pool. This place breathes tranquility and relaxation. Since you normally travel by car in this country anyways, everything is close by.
I'm going to keep this fairly short but what I will say is if you are going to stay in Palm Springs please stay here. It's not right on the main drag but it's in a lovely residential area, no noise, ample parking and just so peaceful. Only 5 in an Uber to the main strip with the bars and... More
We had unit 4 on the east side of the complex for 3 nights - very quiet, very comfortable bed, nice amenities in room - killer shower!! pool was large, heated, wonderful - Judy hope I got that right made us fresh orange and banana smoothies when we were in the pool - breakfast in fridge was just ok, little... More
Stayed 3 nights in this beautiful hotel. This place is very clean, rooms have all been recently upgraded. Big comfortable bed, nice kitchen with granite countertops, fridge, Keurig coffee maker, and even a two burner stove. Bathrooms are big with granite countertops, two sinks, and a huge shower. Pool area is gorgeous and the owner and staff make you feel... More
This place is just perfect for everyone looking for some rest in lovely and warm Palm Springs. The host welcomed us very very friendly, explaining us what we could find where. The private kitchen had our breakfast and a complimentary bottle of wine. The room (call it the appartment) had everything and was very well decorated and had an outside... More

"""

def showWordCloud(keys):
  # OPTIONAL - wordcloud including all emotions mentioned in review
  # find common elements from review and all reference lists
  aspects=(list(set(keys).intersection(aspect_list))) 
  frequency_dist = nltk.FreqDist(aspects)
  wordcloud = WordCloud().generate_from_frequencies(frequency_dist)
  plt.imshow(wordcloud)
  plt.axis("off")
  plt.show()  

#use tokenize function to use nlp to convert review to list
keys=tokenize(doc)
keys=[re.sub('[^a-zA-Z]+', '', _) for _ in keys] # remove numbers or special chaar
showWordCloud(keys)  

