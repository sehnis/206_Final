###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.

from bs4 import BeautifulSoup
import collections
import json
import re
import requests
import sqlite3
import unittest

# Begin filling in instructions....

# SET UP CACHING -- Creates the json file to cache data.

CACHE_FILENAME = "206_final_cache.json" 
try:
	# Use the json cache, if it already exists.
	f = open(CACHE_FILENAME,'r')
	cache_data = f.read()
	f.close()
	CACHE_DICTION = json.loads(cache_data)
except:
	# If it doesn't exist, create a new one.
	CACHE_DICTION = {}


# BUILD STATE DIRECTORY -- The parks are divided by their state, so this collects the state information.

	# There is a dropdown list on the index page, within which all of the state urls can be found.
	# This function pulls data from it, and generates a list that later functions can use to pull individual state data from.

def build_state_directory():

	# CHECK CACHE
	if "cached_states" in CACHE_DICTION:
		print("Using cached data for the states...")
		found_urls = CACHE_DICTION["cached_states"]
	else:
		print("Retrieving data for the states...")
		# Scrape the data from the dropdown using Requests and BeautifulSoup.
		state_request = requests.get("https://www.nps.gov/index.htm").text
		state_soup = BeautifulSoup(state_request, "html.parser")
		found_states = state_soup.find("ul", {"role" : "menu"})

		# Get the partial urls from the list's "href" elements, and create full urls from them.
			# Example: "/state/al/index.htm"  -->  "https://www.nps.gov/state/al/index.htm"
		raw_urls = [partial["href"] for partial in found_states.find_all("a")]
		found_urls = ["https://www.nps.gov" + raw for raw in raw_urls]

		# If the program hit this else loop, then the cache doesn't exist and needs to be made like this.
		# This should save a considerable amount of time instead of rescraping every time.
		CACHE_DICTION["cached_states"] = found_urls
		f = open(CACHE_FILENAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	return found_urls

# BUILD PARK DIRECTORY -- This collects data on the individual parks.

	# Now that we have a list of state urls, we can use BeautifulSoup to individually scrape the park entries for that state.
	# This function pulls data from the state pages, and creates a number of lists.

def build_park_directory():

	# A list of url lists is needed to return all of the information produced by this function.
	all_parks = []

	if"cached_parks" in CACHE_DICTION:
		print("Using cached data for the parks...")
		all_parks = CACHE_DICTION["cached_parks"]
	else:
		print("Retrieving data for the parks...")
		# Iterate through the urls found in build_state_directory(), and set up Requests and BeautifulSoup for each entry.
		state_urls = build_state_directory()
		for state in state_urls:
			parks_request = requests.get(state).text
			parks_soup = BeautifulSoup(parks_request, "html.parser")

			# Get the individual parks' urls for the given state.
			# This collection gave errors when shortened, so the lists' code is comparatively expanded.
			park_data = parks_soup.find("div", {"class" : "ColumnMain col-sm-12"})
			raw_parks = park_data.find_all("h3")
			raw_entries = [park.find("a") for park in raw_parks]
			raw_urls = [entry["href"] for entry in raw_entries]
			found_urls = ["https://www.nps.gov" + raw + "index.htm" for raw in raw_urls]

			# Add the list of found urls to the overarching list of park urls.
			all_parks.append(found_urls)

		# If the program hit this else loop, then the cache doesn't exist and needs to be made like this.
		# This should save a considerable amount of time instead of rescraping every time.
		CACHE_DICTION["cached_parks"] = all_parks
		f = open(CACHE_FILENAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	# When done iterating, return the master list of urls.
	return all_parks

# CREATE NATIONALPARK OBJECTS -- Use the state urls to initialize the states.
	
	# At this point, using BeautifulSoup on the park urls gets us all the information we need for the individual parks.
	# Adding them directly to an __init__ function is the most efficient, so the NationalPark object is declared now.

# Create a list of NationalPark objects.
all_urls = build_park_directory()
full_np_objects = []

for parks_per_state in all_urls:
	for individual_park in parks_per_state:
		print(individual_park + "\n")
	print("\n")


#class NationalPark():
#	def __init__(self):
		# self.name = TODO
		# self.location = TODO
		# self.states = TODO
		# self.access = TODO
		# self.contact = TODO
		# self.urls = TODO





# Put your tests here, with any edits you now need from when you turned them in with your project plan.


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)

if __name__ == "__main__":
	unittest.main(verbosity=2)