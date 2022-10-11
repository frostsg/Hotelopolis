import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import functools

# reference:https://towardsdatascience.com/machine-learning-text-processing-1d5a2d638958

# This feature is a work in progress
# - anurag

review1 = """ 
The hotel is just one of many that are on this new trend of firmer pillows and mattresses. This is the third hotel I have stayed in the last few months that have had firmer vs softer mattresses in their rooms. Aside from the bed The room was well appointed, comfortable and really The bonus Those super plushy and comfy robes in the closet. I miss a good hotel robe and this one had one!! Another little thing 
I loved was the spa water and coffee service in the lobby. High quality coffee and the New York Times Count me in! The maid service was friendly, attentive, and I even got a little note. Would totally stay again.
excellent location near convention center. friendly, willing staff. not a true luxury hotel in terms of the room I received, but a comfortable clean room, I didn't really need any more than that. After all you're here to visit San Francisco, not the hotel.
Hotel Zelos was a great place to stay in San Francisco. The staff is definitely the highlight of the hotel. The hotel itself is great: clean, well decorated, etc, but the people who work there were very helpful and friendly. The location is great being right next to the Powell BART station but the neighborhood is under construction. This obviously isn't the fault of the hotel and won't impact your stay. We couldn't hear any of the construction, but it makes it a little more difficult to get around. Overall, I definitely recommend Hotel Zelos!
Pros: the location is awesome, the room size is great, the bathroom is nice also with a nice tub. Bad: the style and furniture starts to get really old, no breakfast despite the high price, the price is high, nothing exeptionnal... We were 4 people and so 4 reservations. Unfortunately one was missing. It was 1am so very bad surprise.... More
"""  # four reviews concantenated

review = """
Pleasant 10 min walk along the sea front to the Water Bus. restaurants etc. Hotel was comfortable breakfast was good - quite a variety. Room aircon didn't work very well. Take mosquito repelant!
Really lovely hotel. Stayed on the very top floor and were surprised by a Jacuzzi bath we didn't know we were getting! Staff were friendly and helpful and the included breakfast was great! Great location and great value for money. Didn't want to leave!
We stayed here for four nights in October. The hotel staff were welcoming, friendly and helpful. Assisted in booking tickets for the opera. The rooms were clean and comfortable- good shower, light and airy rooms with windows you could open wide. Beds were comfortable. Plenty of choice for breakfast.Spa at hotel nearby which we used while we were there.
We loved staying on the island of Lido! You need to take a water is from Venice to get there. From the train station, a boat ride takes 45 minutes but has beautiful views along the way. Hotel is an EASY walk from the boat dock. The room was very clean and the breakfast was plentiful. We would definitely recommend this hotel!
disgusting food. It had a bad experience in the restaurant. They very very expensive too. I will never return
Our experience at Rancho Valencia was absolutely perfect from beginning to end!!!! We felt special and very happy during our stayed. I would come back in a heart beat!!!
Amazing place. Everyone was extremely warm and welcoming. We've stayed at some top notch places and this is definitely in our top 2. Great for a romantic getaway or take the kids along as we did. Had a couple stuffed animals waiting for our girls upon arrival. Can't wait to go back.
We booked a 3 night stay at Rancho Valencia to play some tennis, since it is one of the highest rated tennis resorts in America. This place is really over the top from a luxury standpoint and overall experience. The villas are really perfect, the staff is great, attention to details (includes fresh squeezed orange juice each morning), restaurants, bar and room service amazing, and the tennis program was really impressive as well. We will want to come back here again.
Currently in bed writing this for the past hr 1/2 there have been dogs barking and squealing call the front desk to advise basically to be told there's nothing they can do. 315.00 and I can't sleep.
I live in Md and the Aloft is my Home away from home...we stayed 1 night 7-7-16 ...Staff is great ! Especially Olivia who was Extra special because she remembered me by my voice over the phone ...which tells me she is very alert and pays attention to the customer their needs.AND SHE DID ! Thumbs up... More
I stayed here with my family for my daughters wedding. It had a very accommodating staff, Olivia was excellent. The rooms were very well maintained. Would highly recommend this hotel, especially if your wedding venue is Celebrations at the Bay!
Beautiful rooms and the nicest people working there. The front desk lady, Olivia, was extremely patient and helpful. We had lots of questions and she had just as many answers. The rooms were sleek and modern. The only thing that would make this hotel better would be free breakfast, but I really am asking for a lot. A++ stay. Thank... More
We stayed here while visiting Maryland Live!. Cute hotel in a great location. Clean, with a very modern look, upgraded bathrooms and amenities and super nice staff. Would definitely recommend and stay there again!
I travel a lot with my job, so I'm constantly staying at hotels. When my co-workers and I arrived late last night at the Aloft the people at the front desk were more than welcoming. When I wanted to order room service I was told it was too late however, Olivia at the front desk informed me of a Italian... More
In my line of work, I use meeting space in hotels often. In my 15+ years of doing this work, this is the first time I've felt the undeniable pull to go out and write a hotel review, based solely on my meeting room experience. Though I did not use a guest room here, my colleagues who did shared that... More
The staff is very friendly and helpful. The rooms are large and nicely furnished. Feels new, as if we were the first to stay there. Actually it is more opulent than I require. The free breakfast was good with sufficient choices including fresh fruit salad, eggs, bacon, bagels and pastries and more. It was a great location for our purpose:... More
Very friendly staff, great free breakfast items each morning, room and facilities very clean, staff superb! We had a problem with the heating system in our room and they had someone fix it within minutes! Would highly recommend this location/hotel.
Upon arriving I see modern yet elegant decor which is pleasing to the eye. The front staff are very friendly. The room was clean including details, I'm talking no dust,no hair in bathroom-shower or beds which I tend to find in other hotels. Kudos to housekeeping. Sheets were crisp,beds were comfortable especially since this is a newer hotel. Breakfast in... More
This is a nice hotel with great staff. I have young children and the entire staff from the front desk staff to the breakfast staff were there to help us. This was our first visit to the Portland area and we plan to go back later this summer. We will stay at this hotel when we return.
Beautiful property and every staff member I encountered (front desk, housekeeping, breakfast hosts and GM) provided beyond excellent customer service! It's also conveniently located near restaurants, grocery stores starbucks and is a short drive to the freeways. I will definitely be back!
Old hotel with many remaining architectural charms and most modern amenities. The staff is exceptional: friendly and very accommodating. Has a little bit of the wear tear around the edges associated with an historic building but remarkably clean. Passed the allergy test.
Very comfortable room. Our son came and they had a couch that they pulled out into a queen size bed. Free wifi and bottled water. This hotel was built back in the 20's and the decor is fabulous. A very neat hotel.
Stayed here for second time recently. Gorgeous lobby. Friendly staff. Good free shuttle service. Our room this time was disappointing. King bed in too small space so that one side did not even have a lamp. Also the heating/cooling unit was right next to the bed and very noisy so we turned it off. Luckily it was not needed. Room... More
My husband and I always try to stay at the Hotel Phillips when we are in Kansas City. It is our favorite hotel and we have stayed at many. I feel at home there and the staff has always been exceptional, although we are not particularly demanding guests. Over the years we have probably spent at least 20 nights there.... More
Just stayed one night but very happy. Nice, comfortable top floor room. Staff could not have been more helpful. Great location right by the Power Light district. Be prepared to pay for valet parking. Price of this was Offset though by free wine and cheese reception.
Everything was sold out in State College for Garth's concerts and the Inn came up as available...what an amazing find!! I'll be making the drive now each visit, just to stay there! The Inn is wonderfully decorated and I so enjoyed browsing all the books. Breakfast was amazing each morning. Thank you Stephanie and team!!
I work here in Perry about 6 days out of the week. The People here are very friendly and willing to make your stay better. The hotel is great for my simple needs as I'm away from home. The rooms and hallways smell very clean each time I enter and leave. I will continue my business here for sure.
The hotel is just one of many that are on this new trend of firmer pillows and mattresses. This is the third hotel I have stayed in the last few months that have had firmer vs softer mattresses in their rooms. Aside from the bed The room was well appointed, comfortable and really The bonus Those super plushy and comfy robes in the closet. I miss a good hotel robe and this one had one!! Another little thing I loved was the spa water and coffee service in the lobby. High quality coffee and the New York Times Count me in! The maid service was friendly, attentive, and I even got a little note. Would totally stay again.
excellent location near convention center. friendly, willing staff. not a true luxury hotel in terms of the room I received, but a comfortable clean room, I didn't really need any more than that. After all you're here to visit San Francisco, not the hotel.
Hotel Zelos was a great place to stay in San Francisco. The staff is definitely the highlight of the hotel. The hotel itself is great: clean, well decorated, etc, but the people who work there were very helpful and friendly. The location is great being right next to the Powell BART station but the neighborhood is under construction. This obviously isn't the fault of the hotel and won't impact your stay. We couldn't hear any of the construction, but it makes it a little more difficult to get around. Overall, I definitely recommend Hotel Zelos!
Pros: the location is awesome, the room size is great, the bathroom is nice also with a nice tub. Bad: the style and furniture starts to get really old, no breakfast despite the high price, the price is high, nothing exeptionnal... We were 4 people and so 4 reservations. Unfortunately one was missing. It was 1am so very bad surprise.... More
After getting the bait and switch I decided I'd rather stay anywhere else. I'm sure I wasnt missing much as it looks like project style crack house apartments. The front desk (old middle eastern lady) was extremely rude and up charged me 50 when I got there! I travel and stay in hotels 250 days/ year and trust me this... More
We had no choice but to stay here when a tornado hit the area and most of Vineland was without power. They charged us 190 for one night, wouldn't accept my AAA card and after leaving, we found out, we had been charged for 4 cats (which we don't own) and for another person. It was only my husband and... More
Hotel is in the perfect spot at the perfect price with the not so perfect view. Expedia rep said that it was facing the water and in a way it was but at a 45 degree angel past the parking lot and a few other obstructions. You have to stretch your neck at the furthest corner of the window to gain a peak. But it was still good though. The room sleeps like nobody's business. Once your head hits the pillows its light out. What I did not like was the front desk personnel. They really did not like there job and it showed. No eye contact, no smiles, no small talk, and what really disturbed me was at check in when I was told to sign this that's how it was put. I was like what is it Just sign - its nothing. Sir What am I signing. Oh if you have a party and smoke we can charge you 250.00(eyes still on monitor). Well sir. Tell me that. Next. Came back later that night to get snacks out of the cupboard. Over priced but I expected that but the person at the front desk was lifeless and didn't not even give me a total. She just says. Its charged to your room and kept staring at her monitor(again the monitor). WOW. But what makes up for some of the small inconsistencies is that fact that the water is in walking distance. The Ferris wheel is right there and Gaylord Hotel is right across the street. Good energy in the area and great spots to eat(Redstone) . Cant wait to visit again. Thanks for the snacks!
Excellent experience. Will come again and book stay in the future
heat in room did not work properly, tv remote was broken excessive noise
Even though we were having problems, i.e. Feather allergy, Flat tire, key not working...the front desk personell were always gracious and helpful.
Brand new hotel in brand new retail area on the water. Easy to access off the beltway. Friendly staff, clean rooms, comfortable beds. Only complaint is that the full offering of the Hampton Inn breakfast was not available at the two times we came down (at 7am and 9am on a Saturday). The food at 9am had been in the bin too long. Still more choices than the continental breakfast at other places, including make-you-own waffles and yummy egg burritos. The fee for parking in the community garage was free with room key and even included a convenient room key drop upon final exit. Pool but no hot tub.
It was a great stay
My sister came into town so we decided to go to The National Harbor for a night. Checking in, the hotel staff was very pleasant. Parking is in a garage behind the hotel, for 18. Our room was clean with nice views. The bed was very comfortable. We were able to walk comfortably to the harbor and sightsee. There are also restaurants and bars within walking distance. Breakfast was great, with canadian bacon and sausage patty meat options. There was also a waffle station, eggs, potatoes, fruit, yogurt, cereal, muffins, and other pastries. Checkout was a breeze, and the front desk staff again, was very pleasant. I very much enjoyed my stay and I will definitely return!
Free breakfast! Attentive staff Fantastic location
Excellent experience. Due to a mix-up on my part with the online travel service it was set up as a king rather than two queen beds, for two guys. I immediately called at the time and Hampton said they would make a note that a room with two queens was needed. When i got there, they didn't have a 2-queen room so they put me up in another king room (and my buddy stayed in the original room) at NO additional expense, and I moved to a 2-queen room the next day. That is awesome, customer-oriented service.
The room was really big and clean. The staff was great. The hotel offers free breakfast that was really good ( not the usual crappy free breakfast) The only thing I didn't like about the room was that the air conditioner was regulated a motion sensor. We happened to be staying here on one of the hottest days of the year. The unit only stays on if the motion censor registers a person being in the room. Upon arriving the room was hot. It took about 20 mins for it to cool off. Also the AC cut off during the night when we fell asleep (No movement). I woke up in a pool of sweat and had to get up a walk around periodically to keep the AC going. That really sucked..
THE LOCATION OF THE HOTEL WAS OUTSTANDING. BUT THERE IS AND ADDITIONAL COST FOR PARKING JUST KEEP THAT IN MIND . IF YOU PAY FOR PARKING AT THE TIME YOU CHECK - IN BE SURE TO HAVE IT OUT BEFORE 1 PM THE NEXT DAY
was too quick, but very nice area
clean, good area, very kind crew, easy to park
We had a great overnight trip to the National Harbor near DC. All of the sites and entertainment were within walking distance!
I loved my stay VIP service all the way. I didn't want to leave. I can honestly say I will visit again. I give it 5 stars
The only problem I have was their sensorize INNCOM thermostat for air conditioning unit to start-up. If there are not movement inside the room, it will not kick in..... sucks!! the trick is, you have to keep moving while sleeping to keep the AC running (LOL)....
Convenient and comfortable. Staff is great, breakfast and WiFi is a bonus.
Loved this place! If you are looking for a chain hotel, THIS IS NOT for you. If you are looking for different, unique, friendly, fun...then this is it. We chose the little room with Queen bed, no windows..and it was GREAT. Best bed I've slept in while traveling in a long long time. Although there are internal hotel noises every once and a while..it was by no means disturbing or loud. Location was awesome! We mainly hung out on Decatour street/Jackson square/French market..but even bourbon street was a short walk. Hotel staff is very knowledgeable about places to eat and things to do. We didn't drive here so no idea about parking or valet. Staff was extremely friendly. It's just a super little gem in a crazy town.
Great hotel. So much more character than staying in one of the big chain hotels. The building was a transformed warehouse, so walls are old brick, floors are resurfaced wood, etc. Very Cool. Super helpful staff. Great coffee shop restaurant downstairs. Definitely will return.
Nice hotel with a great restaurant! Only thing that would have been nice to have it a bathtub rather than just a shower.
Pros- Great customer service, comfortable beds, clean rooms, fantastic room style/decor and safe area. Cons- no pool, no meals available, just a few pastry type items at the bar/lobby
The young, hip hotel guests probaby cringed when they saw me schlep my 4, 6, and 8 year olds through the front door and I immediately realized our family was not the hotel's target demographic, but we LOVED this place. As a former New Orleans resident, this is as local as you can get. Compar Lapin was unbelievable and my children could not get enough of their homemade pasta and gnocchi and probably would have gone home with our server, Clare (that is how much they liked her). The head cocktail crafter, Abby, was super friendly and insanely adorable and her staff was extremely talented and helpful. The room was so comfortable my children slept almost two hours past their norm, which was probably appreciated by the majority of guests who had been tearing up their livers the night before. We did not use maid service so my only suggestion would be a little more counter space in the bath and more towels. Other than that, it was perfect.
Bad: Better return from the slots!!. Good: Bed excellent, pillows good, shower good with strong flow and hot. Very well maintained public spaces with lots of wood panelling. The piece of the Berlin Wall was quite interesting and all at a very good price.
Bad: Thumping music all night long. So loud the windows vibrated.
Bad: Losing money lol. Good: I like the attitude and service from the staff...i enjoy the atmosphere and the food
Good: The staff at the place is extremely friendly.Paradise Restaurant buffet good selection, good food, and reasonable cost.
Bad: The room I booked was a non-smoking but when we got to the hotel, the gentleman at the counter said they didn't have any and have not had any available for several days. The guy then said that in order for me to get my money back, I'd have to go through the third party that I booked the room through. Good: Nothing
Good: HELPFUL STAFF
Bad: That the tv would not switch to the input channel. I wasn't able to use the HDMI port on the TV. Good: The company I had with me. Lol
Good: Best gambling in Vegas and best comps! Brewery is great, rooms very clean, staff is wonderful. I only stay at Main Street.
Bad: I still really hate the cigarette smoke in the casino. But other then that (and all the crazies on the fremont experience at night) its fun and awesome!. Good: Location was perfect for our leisure trip. Free valet parking is always amazing (of course we tipped every time we picked up and dropped off our car!) The amount of things to do on the Fremont Experience is endless! What an awesome experience. Truly the 9th island for Hawaiians like us! We love it!
Bad: 1st - PARKING LOT **BAD,BAD,BAD** This is 2017, nobody need driver to parking car, unless you're 85 yrs old (should not even drive). But drivers that steals quarters from your rental car, this is very low. 2nd - They asked a deposit of 100. Because I was planning to get it back, I used a BC and not a CC. On check out I was informed that it will take 1 to 2 days. Should I trust on it 3rd - If you sleep on that room 512 and need a AC on, make sure you are deaf or use to leave near NY freeway. The noise of that machine it's worst than sleep on LV international airport at 9am with your windows car open. Will I stay on this hotel again NEVER. Good: Location, access to shopping, and cleanning
Bad: Dirty and old room. Valet parking is not comfortable. Casino is old and has no roulette. If you have a car, you can stay, cause the price is everything. Good: Pretty cheap for Las Vegas
Bad: The hotel is very tired - could use an update. Now, I understand why such a deal. Can not figure out higher rating given to it overall. Good: Location was in the middle of the Freemont Experience.
Bad: Not much. Good: For several years, a group of us has met for the SEMA SHOW. We have always come over a day early, and met for fun and dinner at your 777 Microbrewery. This time we were booked at MAIN STREET STATION as well.We'll be back, particularly since you didn't charge resort fees.
Bad: Check out was too slow. Good: Buffet was excellent
Bad: To be honest, nothing to complain about. Just too bad that there wasn't any free wifi in the rooms. Good: Considering that we only paid 88 dollars for 2 persons for 2 nights, this was great value for money. The hotel is located in the middle of Fremont Street, so you just step outside and you are in the middle of the action. Our room was on the 9th floor and we didn't hear any noise whatsoever. The room was maybe a bit old fashioned, but still offered everything you need. We were positively surprised that we had access to the pool and gym of the California hotel. We just needed to walk 2 mins to access their facilities. The gym was really good equipped for a hotel gym. Pool was really nice and quiet. Would definitely stay here again!
Bad: This room is straight out of a horror film. Good: I like Fremont st
Bad: nothing!. Good: buffet is excellant! room are clean, great view of mountains and saw fireworks in distance.
Bad: access to parking. Good: the location
Bad: Very satisfied.
Bad: The place was falling apart, the tub was cracked and broken. the bathroom shelf was barely holding on. The bed was extremely tough to sleep on. Good: I liked that it was close to entertainment. The shower held a hot water temperature for a long time.
Bad: Bathroom was small, noisy outside. Good: Location, beds, price
Bad: The parking garage is so hard to find. I passed it at least two times trying to find it. You also can't self park, which is a hassle coming back from being out and about. You have to rush to gather all of your belongings, souvenirs, etc, because the entry bay to the garage will hold two cars at most. You can't dilly dally. Hope that makes sense. Only paid WiFi,which was a big bummer. The express snack bar/grill staff were very unfriendly. Every time I went to the buffet, the line to be seated was always sooo long. I never did end up eating there for that reason. Good: Near all of the Fremont Street Experience stuff.
Bad: The cleanliness wasn't the best. One of our towels and bed sheets had red stains on them which the staff informed us was rust, and not blood....upon arrival the toilet wouldn't flush as well. We got stuck in a smoking room even though we didn't book a smoking room. The noise was unbearable, and when combined with the smoke just added up to disaster. Good: Close to the public transportation systems. In the middle of downtown Las Vegas.
Bad: smokey air out of elevators. Good: valet parking with security-
Bad: Not sure about deluxe room i was in. Good: Location
Good: Close proximity to Freemont Street Experience.
Bad: missed not having a pool or somewhere to sit out and read. we were next to the railway so the train was noisy but we got used to it. Good: loved the food. beds very comfortable. excellent value.
Bad: I lost roulette. Good: Buffet bb
Bad: The bathroom needs to be upgraded. It is very worn, the brown wall paper was dirty and the paint on the sink counter was pealing off. was also disappointed the room did not have a coffee maker. I like to have a cup while I get dressed in the mornings. would have liked a non-smoking area in the casino. I am a non-smoker and I had to keep taking breaks and go outside for fresh air. Good: The Beds were great! The location was very good. The gentleman at the Registration desk was very helpful and friendly. And the Lady at the Keno lounge was nice too.
Bad: Not so quiet during the night, since it's really close to highway. Good: The beds were very confortable. The parking was for free, and the location close the Fremont street.
Bad: The beds were not too comfortable. Good: I really liked its location, and slot machines, the Paradise Buffet, and Duncan Donuts place within the Fremont Hotel.
Bad: The elevator to the parkade requires some maintenance - at least a wet mop to kill whatever is lurking on the floor!. Good: This resort hotel is amazing - the location in perfect, the rooms are huge, and absolutely spotless!
Bad: Limited TV channels and no refrigerator or coffee making facility in room. Good: The free parking at the hotel was great and all the staff were very helpful and polite.
Bad: Small restroom. Good: Clean room with a great view.
Bad: Even though we got a non smoking room it still smelled like smoke. Good: Valet parking Duncan doughnut
Bad: The hotel bathroom should be remodeled as the bathtub looks quite old. The drain gets clogged easily, and the basin tap handle looks like it is about to fall apart. No free WiFi. No fridge. And even no coffee-maker/kettle. Good: Good location with a few minutes walk to the Mob museum. The hotel is located in the heart of Fremont Experience. Both northbound and southbound bus stops are just beside the hotel building. Besides, the staffs are quite friendly. The buffet was satisfactory, and the price is cheap due to the 10 off for guests every meal.
Bad: It was hard to get into the parking area because of traffic (an event was going on) no coffee pot in the room. I like to sit and drink coffee for and hour or so before doing anything for the day. I'm not paying 3.00 per cup of coffee. Other than that it was ok. Good: It was a beautiful hotal
Bad: Nothing. Good: Location on Fremont
Bad: Rooms small, air conditioning don't work!!.
Bad: Old, not many outlets. Good: Location and price.
Bad: No business center..wifi wasnt free..it asked for ten bucks...the internet kiosk was 650 for 30 mins..but deducted 20 mins to print boarding passes and no shuttle to airport. Good: Location
Bad: I was in room 314, and its very noisy at night with the street ambiance, so dont expect to sleep before 2AM. I had to take my breakfast to adjacent hotels as continental / seated proper breakfast was not available (or couldnt find it...). Good: The bed was confortable and the location is just amazing on Fremont street.
Bad: Main Street Station recently implemented paid parking (I stayed last week and it was still free). Although parking is free for hotel guests, they have not worked the kinks out of the system. We almost missed our flight due to being unable to leave the lot. Security had to be called and that person told us that there have been a large number of similar episodes. They need to FIX this!. Good: Everything EXCEPT the parking.
Bad: none.
Bad: Th e food wasnt that good. Good: The breakfast buffett was good, the other 2 restaurants were just fair, in fact in one of them I got sick with the food.
Good: The rooms were very comfortable, clean, and well maintained
Bad: There's nothing not to like here. Though the maid service was good but they are kind of early to knock at the door for cleaning service. They're there at 8am and we were still in dreamland that we were forced to get up and open the door to talk to them to clean later. Good: We love our very spacious room though we didn't have a single king sized bed. They gave us twin beds but it's fine. The Garden court buffet was also great! It was very affordable. We almost eat there everyday because of its price. Please keep it that way.
Bad: The airconditioner in the room did not work, and it made a very loud sound all night. We told the front desk and they were able to fix it for the next night stay. It's understandable because the hotel itself is very old. We would probably stay in a different hotel when we go back. Good: Staff was very helpful and nice. Tony Romo's restaurant was very good.
Bad: Bed was not comfortable - they need to replace the mattress. Good: Room was clean.
Bad: The entire place smells like an ashtray. The rooms were small and the place is noisy. It's a complete freak show under the canopy---ugly people who are 90 nude with no talent. Wall to wall beggars and hawkers. The entire Las Vegas is full of annoying street hustlers and creeps. What a waste of our First Amendment Rights! Next time I go to LV, I will stay in a South Vegas Hotel, go to a show and leave the next day. Too bad Vegas is stuck with such a beggar and homeless problem. Good: It was on my bucket list and I wanted to experience the canopy light show---ok, check it off. Good deals on food: Tony Roma's is located within the Fremont Hotel and steak and lobster for 11.99 is a DEAL! The Valet Parking was free and excellent. The entire Staff was excellent but seemed embarrassed to be in such a dump. It was cheap but you pay for it if your not a smoker.
Bad: The bathroom is very small, smaller than I am used to. The saimin noodle soup at the cafe was terrible, the noodles were mushy and blend. Good: Location was right. The buffet was so so. The food at the cafe was okay. The rooms are kind of small but okay.
Bad: The pool was not at the hotel had to go to another hotel to swim and that is not stated when your booking your room. Just make it clear that there is not a pool at the hotel other than that loved the hotel!. Good: Great place to stay
Bad: in old town, far away from new main strip noisy air-con in room decor abit old. Good: cheap buffet with good quality big room comfort bed
Bad: The bed was stiff and valet parking only. Wifi is pay only and didn't live up to the speed expectations as advertised. Good: The location is great, easy access to all of Fremont area with a short walk. Not being a giant casino you don't have to walk far from the car or through the place to get out.
Bad: Extremely disappointed in Fremont Street. It used to be my favorite place to play/stay in Vegas but I will not be back. Very strange people just standing in the middle of the street. Cartoon characters, men in thongs and even one in an adult diaper! It's Hollywood Blvd on steroids! Thanks for the memories, Downtown Las Vegas. The Fremont Street Experience is one I do not wish to repeat!. Good: The hotel was very nice, much nicer than The Plaza next door.
Bad: My room was near the ventilation system and there was a lot a noise coming from that. Good: Excelent location in the freemont Experience.
Bad: There were a couple younger staff at the desk during mid day times that seemed bothered by questions. Good: Easy to park. The room was clean and cool. Valet staff was really nice. Steve the maintence man was amazing. I dropped my pearl earring down the bathroom sink. He took the time to take the loop of the drain and get my pearl earring back. I was grateful for his extra service and care.
Bad: Waitress didn't come around a lot even with tipping. The hotel was older and had some cosmetic problems. Good: Lots to around the property and decent food prices. The buffet was really good.
Bad: When we left there was a valet parking worker that made us put are luggage on the cart. But other than we had an awsome time there. Good: The location and the restaurants were great I enjoyed the buffet!
Bad: Rude staff. Cleaniness. Bed. Had to change rooms three times. I will never stay there again!. Good: Nothing
Good: Good hotel at Fremont street. But do not expect something special. Relatively old rooms, no WIFI in the rooms, but the bed was comfortable, the staff was nice, and the Hotel is direct in the heart of Old Las Vegas.
Bad: Pricey, but it was fathers day weekend. Good: Access to downtown
Bad: No pool. Good: Every thing was walking distance
Bad: Dirty, tiny bathroom and no pool. Good: Prime rib meal deal at Roma's
Bad: A fridge in the room would be super nice. Good: The room was very clean, beds comfy and 3 pillows. Every one was friendly. Great valet staff.
Bad: The bar is a little on the expensive side. Drinks are very small for the price. The bartender we had was very slow and not very friendly. We waited about 10 minutes before we were served. It wasn't busy either. Good: Staff was very nice and helpful. The location of the hotel is very convenient.
Bad: I loved everything. The parking, the restaurant ,the rooms and the the several acts that perform every night in the downtown area. Good: The people at the front desk were superb. They upgraded me to a real nice room.
Bad: the noise fm the live bands when trying to sleep.
Bad: Might need a little updating. Good: Conveniently located on Fremont
Bad: Better meal choices. Pool and fitness center on property. Good: Ease of conveniece to everything I needed
Bad: That I had to leave great place. Good: Everything very nice room food service
Bad: There is handicap parking for checking in but not close after checking in. Good: Everything was convenient and costs of the buffet were not bad. Prices in the restaurant were affordable.
Bad: My money was stolen at the valet... room was dirty and had to get another then key card didn't work for new room. Manager did his best but I was disappointed. Good: Location
Good: The hotel is really beautiful! A little old, but clean and comfortable. The price is also good.
Bad: safe is too small for dslr camera or laptop. not acceptable. Good: good location, good food, good price
Bad: The bar tender in the Casino was not at all friendly or attentive. Good: very nice restored hotel. Excellent condition. Great atmosphere. A very nice place to stay in Downtown Las Vegas
Bad: rooms are dated, not as clean as I like. casino is crowded - too many machines.
Bad: Not a thing. Good: The room was nice and clean, bed was very comfy. The restaurants were all great the Buffet was awesome.......... So much to do in the aera
Bad: Shower Tub clogged. Good: Convenient location. Reasonable food prices. Awesome selection of cuisine. Helpful staff!
Bad: Hassle checking in confirmation email lost by bookings or Fremont hotel had my email almost didn't use mine scary .
Bad: Rude staff. Couldnt find our reservations waited 2 hrs to confirm eventhough prepaid..rooms not cleaned. Got smoking instead of non smoking. Will not be staying there anytime soon not. Good: Location
Bad: Room was a lot smaller than I expected, and seemed a bit rundown. Not to mention we were supposed to be on a floor that was nonsmoking. The floor smelled of a smoking lounge. Good: Location and staff were awesome. Had a great view of Freemont street from our room.
Bad: The ventilation system was not adequate for the building. Everything including room smelled like cigarette smoke. Good: restaurant
Bad: The room was hot the ac didn't work . the beds looked like full beds had to put both together . other than that everything else was fine. Good: It was nice staying at the Fremont loved going out to the street to see everything happening all the bands playing never did that before .
Bad: Valet scrapped my car on the wall and no fridge in the room. Good: It was clean and close to everything!
Bad: Non smoking rooms smelt like smoke and just all the cigerate smoke throughout hotel. And room drains slow draining. Good: I liked the lanai restaurant and valet parking
Bad: The wait to enter the buffet was too long never got in the whole week.. When I went to the other restaraunt I was told I couldn't order certain items as they are for happy hour only so I left. They also did not have a pool or any alternative except travel 18 miles to their other facility and use their pool. They never even gave me a discount for lack of this facitilityor even notifying me as I made my reservation months in advance, I also did not like having to park outside of the parking garage only cause I was riding a motorcycle the parking garage was for cars only. I felt as though I was a second class citizen, no laundry facility service or machines . Good: The location was good and the staff especially the cleaning of my room was great.
Bad: Short staffed at the registration desk. Good: Great location and price was right
Bad: It's not the hotels fault, but the sirens on the street woke me up. Good: The best bed I've slept in besides the one at home! Enjoyed all the pillows! Even though the hotel is older, the room was fine! The bathroom was generous, with a good shower.
Bad: The cleanliness wasn't the best. One of our towels and bed sheets had red stains on them which the staff informed us was rust, and not blood....upon arrival the toilet wouldn't flush as well. We got stuck in a smoking room even though we didn't book a smoking room. The noise was unbearable, and when combined with the smoke just added up to disaster. Good: Close to the public transportation systems. In the middle of downtown Las Vegas.
Bad: No self parking.. had to reach down to flush toilet. Good: Location
Bad: The bathroom was gross. The inside of the tub was peeling.The ceiling looks as if it had a previous flood upstairs. Good: The buffet was good.The location of the hotel was great.
Bad: We liked everything. Good: The beds were comfortable the rooms were clean
Good: The location was easily accessible to any downtown activities and the strip, we went to the pinball neon museum and the fremont street experience in one day. It was great
Bad: Old outdated rooms, even though its a classic hotel does not mean they dont have to put forth effort to modernize rooms. Good: Was right in Fremont street
Bad: One of the things we did not like was the fact that we couldn't wake up to a cup of coffee in the morning without paying an arm and a leg for one. The other was that they should at least offer free coffee and beverages to their customers. Washington State casino have a coffee and soda machines for their customers to enjoy as they play. I also do not like the idea of casinos shoving resorts fees down a person throat when they know that the percentage of customers do not use the resorts. Good: I enjoyed the friendly staff.
Good: The hotel room was spacious and very comforting.....
Bad: We hated the window were fake. Good: I liked the location the most
"""

# reference lists
restaurant_list = ['Restaurant', 'Food', 'Coffee', 'Tea', 'Breakfast', 'Lunch', 'Dinner', 'Buffet']  # ref list for restaurant filter
pool_list = ['Pool', 'Swimming']
jacuzzi_list = ['Jacuzzi', 'Hot tub', 'Tub']  # ref list for pool filter
gym_list = ['Gym', 'workout', 'exercise', 'treadmill', 'dumbbells']  # ref list for gym filter
spa_list = ['Spa', 'health', 'sauna', 'massage']  # ref list for spa filter
facility_options = {1: restaurant_list, 2: pool_list, 3: jacuzzi_list,  4: gym_list, 5: spa_list}
neg_emotions = ['unaffordable', 'disgusting', 'bad', 'poor', 'expensive', 'dirty', 'sad', 'uncomfortable', 'rude','hassle', 'horrible', 'noisy']
pos_emotions = ['affordable', 'good', 'comfortable', 'nice', 'beautiful', 'luxury', 'happy', 'joy', 'lovely','friendly', 'helpful', 'pleasant', 'awesome']

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
    stop_words = set(stopwords.words('english'))  # remove unimpt words e.g 'a, the, for, to'
    tokens = [word for word in tokens if not word in stop_words]  # remove unimpt words e.g 'a, the, for, to'
    tokens = [*set(tokens)]  # remove duplicate words
    return tokens

def facility_check(reviewlist):
    facility_list=[]
    #global review, restaurant_list, gym_list, spa_list, pool_list, facility_options

    # NLP to convert review into tokens
    tokens=tokenize(reviewlist)

    # user options 1 for restaurant, 2 - pool, 3 - Gym, 4 - Sauna
    options = range(1, 5)
    counter = 0
    # if user input is 1, then it compares review words with strings in restaurant list "1:restaurant_list"
    for key in facility_options:  # if key of the ref list matches with user option
        counter += 1
        if key == counter and counter <= 4:
            fac_list = ([x.lower() for x in facility_options[counter]])  # converts strings in list to lowercase
            # expected result : True or False (true - means the facility is found in the review)
            if (common_item(tokens, fac_list)) is True:
                facility_list.append(fac_list[0])  # append the facility to the prev created empty list
            else:
                continue
        else:
            break
    return facility_list

def showwordcloud():
    # OPTIONAL - wordcloud including all emotions mentioned in review
    aspects = (list(set(tokenize(review)).intersection(pos_emotions + neg_emotions)))
    frequency_dist = nltk.FreqDist(aspects)
    wordcloud = WordCloud().generate_from_frequencies(frequency_dist)
    plt.imshow(wordcloud)
    plt.axis("off")
    # uncomment below for word cloud to appear
    plt.show()

"""


# display common words from 2 sets/lists - tokens (review) and facilties
# print("Hotel Facilities are: ",(list(set(tokens).intersection(facilities))))
# showing good aspects from review
# print("\nGood aspects: ",(list(set(tokens).intersection(pos_emotions))))
"""
