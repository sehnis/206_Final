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
import codecs
import collections
import json
import re
import requests
import sqlite3
import sys
import unittest

# From Piazza -- combats codec errors for Windows.
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

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

		# Get the partial urls from the list's "href" elements, and add the base to them.
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

	if "cached_parks" in CACHE_DICTION:
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
			found_urls = ["https://www.nps.gov" + raw for raw in raw_urls]

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

class NationalPark():

	def __init__(self, url):

		# Recreating all of this information every time the program is run would take forever,
		# so caching is used as it was before (large cache file, but more reasonable requests.)
		dict_key = url + "_data"
		
		self.park_url = url

		if dict_key in CACHE_DICTION:
			# Data is stored as a dictionary in the cache, so retrieve it if it was already found.
			self.name = CACHE_DICTION[dict_key]["n"]
			self.park_type = CACHE_DICTION[dict_key]["pt"]
			self.states = CACHE_DICTION[dict_key]["s"]
			self.address = CACHE_DICTION[dict_key]["a"]
			self.phone = CACHE_DICTION[dict_key]["ph"]
			self.planning = CACHE_DICTION[dict_key]["pl"]
			self.has_phone = CACHE_DICTION[dict_key]["hf"]
		else:

			# As before, scrape the supplied url.
			np_request = requests.get(url + "index.htm").text
			np_soup = BeautifulSoup(np_request, "html.parser")

			# One specific div contains info on the name, park type, and state.
			# Not all parks have all three, so this may be incomplete at times.
			np_ntl = np_soup.find("div", {"class" : "Hero-titleContainer clearfix"})
			try:
				self.name = np_ntl.find("a", {"class" : "Hero-title"}).text
			except:
				self.name = "[Unnamed Park]"
			try:
				self.park_type = np_ntl.find("span", {"class" : "Hero-designation"}).text
			except:
				self.park_type = "national park"

			try:
				self.states = np_ntl.find("span", {"class" : "Hero-location"}).text
			except:
				self.states = "the United States"

			# Another div has both the address and phone number.
			np_ap = np_soup.find("div", {"class" : "ParkFooter-contact"})
			try:
				self.address = np_ap.find("div", {"itemprop" : "address"}).text.replace('\n', ' ').strip()
			except:
				self.address = self.states
			try:
				self.phone = np_ap.find("span", {"itemprop" : "telephone"}).text.replace('\n', ' ').strip()
				self.has_phone = True
			except:
				self.phone = "[Phone Unavailable]"
				self.has_phone = False

			# Different parks have varying levels of information for safety/accomodations.
			# This program is currently just saving the text on the "plan your visit" page.
			# This page contains an overview of the accomodations and warnings, if any exist.
			extra_request = requests.get(url + "planyourvisit/index.htm").text
			extra_soup = BeautifulSoup(extra_request, "html.parser")
			try:
				#print(extra_soup).text
				self.planning = extra_soup.find("div", {"class" : "Component text-content-size text-content-style ArticleTextGroup clearfix"}).text.replace('\n\n', '\n').strip()
			except:
				self.planning = "There are currently no posted warnings or accomodations, but you can contact the site for more information!"
	
			# Cache the information as a dictionary of variables.
			self.full_dict = {"n" : self.name, "pt" : self.park_type, "s" : self.states, "a" : self.address, "ph" : self.phone, "pl" : self.planning, "hf" : self.has_phone}
			CACHE_DICTION[dict_key] = self.full_dict
			f = open(CACHE_FILENAME, "w")
			f.write(json.dumps(CACHE_DICTION))
			f.close()
	
	# When printed directly, this uses several variables for an in-depth result.
	def __str__(self):
		to_print = self.name + " is a " + self.park_type + " located in the following states: " + self.states + "\n\n"
		to_print += "They are located at " + self.address 
		if (self.has_phone):
			to_print += ", and can be reached by phone at "+ self.phone + "\n\n"
		else :
			to_print += ", but do not have a phone number listed.\n\n"
		to_print += "Here is some important information about " + self.name + ":\n" + self.planning + "\n\n"
		to_print += "----------------------------------------"
		to_print.encode("utf-8")
		return to_print

	# Produces a condensed message about the park name and location.
	def short_print(self):
		to_print = self.name + " at " + self.address
		return to_print

	# Produces a condensed message about the park's phone number for printing.
	def short_phone(self):
		if self.has_phone:
			to_print = "You can reach the park at " + self.phone
		else:
			to_print = "There is no phone number available, but you can find more information at the park website: " + self.url
		return to_print

# Create a list of NationalPark objects.
all_urls = build_park_directory()
full_np_objects = []


# TESTING: ONLY MAKE IT FOR ALABAMA FOR NOW, JUST IN CASE SOMETHING GOES WRONG.
alabama = all_urls[0]
print("The following parks are located in Alabama:" + "\n")
for individual_park in alabama:
	temp_np = NationalPark(individual_park)
	print("    " + temp_np.short_print() + "\n")
	full_np_objects.append(temp_np)

'''
for parks_per_state in all_urls:
	for individual_park in parks_per_state:
		temp_np = NationalPark(individual_park)
		print(temp_np)
		full_np_objects.append(temp_np)
	print("\n")
'''


# DATABASE CREATION

# Create the database connection and cursor.
con = sqlite3.connect("206_final_data.db")
cur = con.cursor()

# Clear out any existing tables and create a new one.
cur.execute("DROP TABLE IF EXISTS Parks")
cur.execute("CREATE TABLE IF NOT EXISTS Parks (park_name TEXT PRIMARY KEY, park_info TEXT, park_url TEXT, park_phone TEXT, park_states TEXT, park_address TEXT)")

# Populate the table based on the list of NationalPark objects created.
np_base = "INSERT OR IGNORE INTO Parks VALUES (?, ?, ?, ?, ?, ?)"
for np in full_np_objects:
	try:
		# Get member variables, and condense them into a tuple to be entered into the table.
		p_name = np.name
		p_info = np.short_print()
		p_url = np.park_url
		p_phone = np.phone
		p_states = np.states
		p_address = np.address
		p_entry = (p_name, p_info, p_url, p_phone, p_states, p_address)
		cur.execute(np_base, p_entry)
	except:
		# Error handling should make it so this isn't needed, but this helps with severely broken entries.
		pass

# Commit the changes to the database, then close it.
# This is one location where more data will be added after this portion of the project is complete.
con.commit()
con.close()

# Put your tests here, with any edits you now need from when you turned them in with your project plan.

class TestParkVariables(unittest.TestCase):
	def test_park_url(self):
		url_test = NationalPark("https://www.nps.gov/hobe/")
		self.assertEqual(url_test.park_url, "https://www.nps.gov/hobe/", "Testing that the park's base url is correctly copied.")
	def test_park_name(self):
		name_test = NationalPark("https://www.nps.gov/hobe/")
		self.assertEqual(name_test.name, "Horseshoe Bend", "Testing that the park's name is correctly created.")
	def test_park_type(self):
		type_test = NationalPark("https://www.nps.gov/hobe/")
		self.assertEqual(type_test.park_type, "National Military Park", "Testing that the park's type is correctly created.")
	def test_park_states(self):
		states_test = NationalPark("https://www.nps.gov/hobe/")
		self.assertEqual(states_test.states, "Alabama", "Testing that the park's list of states is correctly created.")
	def test_park_address(self):
		address_test = NationalPark("https://www.nps.gov/hobe/")
		self.assertEqual(address_test.address, "11288 Horseshoe Bend Road   Daviston, AL 36256", "Testing that the park's address is correctly created.")
	def test_park_phone(self):
		phone_test = NationalPark("https://www.nps.gov/hobe/")
		self.assertEqual(phone_test.phone, "(256) 234-7111", "Testing that the park's phone number is correctly created.")
	def test_park_has_phone(self):
		has_phone_test = NationalPark("https://www.nps.gov/hobe/")
		self.assertEqual(has_phone_test.has_phone, True, "Testing that the park's list of states is correctly created.")
	def test_park_planning(self):
		planning_test = NationalPark("https://www.nps.gov/hobe/")
		self.assertEqual(type(planning_test.planning), type("String about planning"), "Testing that the park's planning information is correctly created as a string.")
	
class TestParkMembers(unittest.TestCase):
	def test_short_print(self):
		spr_test = NationalPark("https://www.nps.gov/hobe/")
		self.assertEqual(type(spr_test.short_print()), type("Printable string"), "Testing that short_print returns a printable string.")
	def test_short_phone(self):
		sph_test = NationalPark("https://www.nps.gov/hobe/")
		self.assertEqual(type(sph_test.short_phone()), type("Printable string"), "Testing that short_phone returns a printable string.")


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)

if __name__ == "__main__":
	unittest.main(verbosity=2)
