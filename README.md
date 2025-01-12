# Description
This project utilizes VDOT information regarding traffic accidents and visualizes the location within the state of Virginia. 

# How it works

To begin with this, we will need to make a map. In this case, I will be using leafletjs for handling the map since its free and I do enjoy not spending money. I originally started following the quickstart guide on their [website](https://leafletjs.com/) but then I realized that I will not be needing the entire world map for this, only the state of Virginia. Even though I didn't end up using openstreetmap in the final stage, I will still credit it because I did use it and thought it was super cool. So instead of going with the full world map, I decided to go to this [wonderful website called naturalearth](https://www.naturalearthdata.com/downloads/) where I can download a GeoJSON file for Virginia. I thought it would be good to just get the entire state of Virginia but I actually ended up needing to get the entire US state map with its counties, which is not meeting the vision. For the vision to become true, we need to take the GeoJSON file we downloaded of all the US state counties and filter it by removing every state except for Virginia. I am surprised by the amount of map resources online and that is where [this other amazing website called mapshaper](https://mapshaper.org/) can do just that. After getting that filtered map, we are left with beauty. I would sometimes get lost and added a reset button to set the view back to normal and added the current lat and long of where the cursor is for debugging. And after what was supposed to be only a few hours turned into nail-biting few days, we are have our first step done.

In order to start with making a map full of data, we are going to need some data. Thankfully, [VDOT's website](https://511.vdot.virginia.gov/) presents us with a neatly ordered table that shows us varying amount of information. Even more thankfully, they allow us to download a CSV with our search keywords. From what I have noticed on their website, they label car accidents with the "Incident" label. If we type in that keyword and download the CSV, we are given the location, time and description of the incident. I am assuming here, but I believe that they remove the incident from their table whenever the incident is resolved. What this means for us is that if we download it at hour 06:00 and we have car accident A, if we download it the next hour at 07:00, it will be removed if the accident is no longer present (huge assumption). But for now, we have a CSV file with the accidents and we can use that to map it out.

Now that we have our data and our map, we will need to make them speak the same language. What this means is that we want to be able to mold the data so that it can actually be represented the way we want on the map. In the CSV, we have the county in which the incident occured and the label. Since I am limited by the technology of my time (brain), I am unable to exactly pinpoint where the incident is on the VA state map but I will group it into the county. I am very glad I don't fully understand json but since it has properties, we can actually get the location of the county based off the county in the CSV. We will iterate through each line in the CSV and find its county's lat and long using the json file and place a marker with the description of the label. Due to my oversight, I didnt think about what would happen if there was more than one accident per county, as it would just lead to the markers overlapping in the county. I was thinking that one solution would be to make a tiny offset of the marker but I to stay within the county borders but I remembered that I don't know how to do that, so I went with the more simple solution, storing a dict with a count and reasons of each accident. I will be using this count and display it under each marker made so its clear how many accidents are recorded in each county. 





# Credits

- https://www.youtube.com/@TheCodingTrain
- https://leafletjs.com/
- https://www.openstreetmap.org/
- https://www.naturalearthdata.com/downloads/
- https://mapshaper.org/
- https://511.vdot.virginia.gov/
