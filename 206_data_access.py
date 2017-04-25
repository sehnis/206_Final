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
import webbrowser

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


# PART ONE -- GETTING PARKS

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

# PART TWO -- STATES / WEATHER

# Huge dict of all of the states/territories that have parks.
states_dict = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "American Samoa": "AS", "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Guam": "GU", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",  "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",  "Northern Mariana Islands": "MP", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",  "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",  "Oregon": "OR", "Pennsylvania": "PA", "Puerto Rico": "PR", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Virgin Islands": "VI", "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "[UNKNOWN STATE]" : "UK"}
rev_states_dict= {"AL" : "Alabama", "AK": "Alaska", "AZ" : "Arizona", "AR" : "Arkansas", "AS" : "American Samoa", "CA" : "California", "CO" :  "Colorado", "CT" : "Connecticut", "DE" : "Delaware", "DC" : "District of Columbia", "FL" : "Florida", "GA" : "Georgia", "GU" : "Guam", "HI": "Hawaii", "ID" : "Idaho", "IL" : "Illinois", "IN" : "Indiana", "IA" : "Iowa", "KS" : "Kansas", "KY" : "Kentucky", "LA" : "Louisiana", "ME" : "Maine", "MD" : "Maryland", "MA" : "Massachusetts", "MI" : "Michigan", "MN" :  "Minnesota", "MP" : "Northern Mariana Islands", "MS" : "Mississippi", "MO" : "Missouri", "MT" : "Montana", "NE" : "Nebraska", "NV" : "Nevada", "NH" : "New Hampshire", "NJ" : "New Jersey", "NM" : "New Mexico", "NY" : "New York", "NC" :  "North Carolina", "ND" : "North Dakota", "OH" : "Ohio", "OK" : "Oklahoma", "OR" : "Oregon", "PA" : "Pennsylvania", "PR" : "Puerto Rico", "RI" : "Rhode Island", "SC" : "South Carolina", "SD" : "South Dakota", "TN" : "Tennessee", "TX" : "Texas", "UT" : "Utah", "VI" : "Virgin Islands", "VT" : "Vermont", "VA" : "Virginia", "WA" : "Washington", "WV" : "West Virginia", "WI" : "Wisconsin", "WY" : "Wyoming"}

def build_weather_directory():

	# Create a list of weather forecasts.
	all_weather = {}

	if "weather_data" in CACHE_DICTION:
		all_weather = CACHE_DICTION["weather_data"]
	else:

		weather_response = requests.get("https://www.currentresults.com/Weather/US/average-annual-state-temperatures.php").text
		weather_soup = BeautifulSoup(weather_response, "html.parser")
		weather_table = weather_soup.find_all("table", {"class":"articletable tablecol-1-left"})

		all_states = []
		state_forecast = []

		for forecast in weather_table:
			all_states = forecast.find_all("tr")
			for state in all_states:
				sfa = state.find_all("td")
				for sta in sfa:
					state_forecast.append(sta.text) 
				# Load information 
				try:
					state_weather = sfa[0].text
					state_fahrenheit = sfa[1].text
					state_celcius = sfa[2].text
				except:
					state_weather = "[UNKNOWN STATE]"
					state_fahrenheit = "[TEMP UNKNOWN]"
					state_celcius = "[TEMP UNKNOWN]"

				# Associate both temps with the state name.
				state_temps = (state_fahrenheit, state_celcius)
				all_weather[state_weather] = state_temps

		CACHE_DICTION["weather_data"] = all_weather
		f = open(CACHE_FILENAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	return all_weather

bwd = build_weather_directory()

def state_db():

	# Create variables and commands relating to the database table.
	con = sqlite3.connect("206_final_data.db")
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS States")
	cur.execute("CREATE TABLE IF NOT EXISTS States (state_name TEXT PRIMARY KEY, state_abv TEXT, weather_degf TEXT, weather_degc TEXT)")

	# Turn state information into a tuple, for insertion into the table.
	state_tups = []
	for b in bwd:
		state_tups.append((b, states_dict[b], bwd[b][0], bwd[b][0]))

	# Populate the table based on the list of Article objects created.
	state_base = "INSERT OR IGNORE INTO States VALUES (?, ?, ?, ?)"
	for tup in state_tups:
		cur.execute(state_base, tup)

	# Commit this table, and close the whole database.
	con.commit()
	con.close()

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
			self.state_abvs = list(re.findall('[A-Z]{2}', self.address))
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

			self.state_abvs = list(re.findall('[A-Z]{2}', self.address))

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
		temps = ("?", "?")
		full_state = rev_states_dict[self.state_abvs[0]]
		for w in bwd:
			# print(w[0])
			if (full_state == w):
				temps = (bwd[w][0], bwd[w][1])
		to_print += "The expected forecast is " + temps[0] + " degrees F, or " + temps[1] + " degrees C.\n\n"
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


all_urls = build_park_directory()
full_np_objects = []
for parks_per_state in all_urls:
	for individual_park in parks_per_state:
		full_np_objects.append(NationalPark(individual_park))


def update_db():
	# Create a list of NationalPark objects.

	# Insert the NationalPark objects into a giant list.
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

	# Commit the changes to the database.
	con.commit()


# PART THREE -- ARTICLES

# Declare the article class
class Article():

	def __init__(self, art_input):

		# Recreating all of this information every time the program is run would take forever,
		# so caching is used as it was before (large cache file, but more reasonable requests.)
		dict_key = art_input[0] + "_data"

		if dict_key in CACHE_DICTION:
			# Data is stored as a dictionary in the cache, so retrieve it if it was already found.
			self.title = CACHE_DICTION[dict_key]["ti"]
			self.synopsis = CACHE_DICTION[dict_key]["s"]
			self.url = CACHE_DICTION[dict_key]["u"]
			self.thumb = CACHE_DICTION[dict_key]["th"]
		else:
			# Otherwise, build it from the inputted tuple.
			# BeautifulSoup is handled directly outside of the article creation.
			self.title = art_input[0]
			self.synopsis = art_input[1]
			self.url = art_input[2]
			self.thumb = art_input[3]

			self.full_dict = {"ti" : self.title, "s" : self.synopsis, "u" : self.url, "th" : self.thumb}
			CACHE_DICTION[dict_key] = self.full_dict
			f = open(CACHE_FILENAME, "w")
			f.write(json.dumps(CACHE_DICTION))
			f.close()

# Get all the articles, and build article objects.
article_objects = []
def build_article_directory():

	all_articles = []

	# If article urls already in the cache, use them.
	if "article_data" in CACHE_DICTION:
		all_articles = CACHE_DICTION["article_data"]
	else:
		# Otherwise, setup and use requests/soup.
		art_response = requests.get("https://www.nps.gov/index.htm").text
		art_soup = BeautifulSoup(art_response, "html.parser")

		# Medium Articles
		individual_art = art_soup.find_all("div", {"class":"Component Feature -medium"})
		for ia in individual_art:
			# Get the title, link, and thumbnail src, then combine and cache them.
			art_title = ia.find("h3").text
			art_info = ia.find("p", {"class" : "Feature-description"}).text
			art_url = "https://www.nps.gov" + ia.find("a", {"class" : "Feature-link"})["href"]
			art_thumb = "https://www.nps.gov" + ia.find("img", {"class" : "Feature-image"})["src"]
			art_full = (art_title, art_info, art_url, art_thumb)
			all_articles.append(art_full)

		# Small Articles
		individual_art = art_soup.find_all("div", {"class":"Component Feature -small"})
		for ia in individual_art:
			# Get the title, link, and thumbnail src, then combine and cache them.
			art_title = ia.find("h3").text
			art_info = ia.find("p", {"class" : "Feature-description"}).text
			art_url = "https://www.nps.gov" + ia.find("a", {"class" : "Feature-link"})["href"]
			art_thumb = "https://www.nps.gov" + ia.find("img", {"class" : "Feature-image"})["src"]
			art_full = (art_title, art_info, art_url, art_thumb)
			all_articles.append(art_full)

		# Create and append the article objects to a list.
		for each in all_articles:
			article_objects.append(Article(each))

		# Update the cache.
		CACHE_DICTION["article_data"] = all_articles
		f = open(CACHE_FILENAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	return all_articles


# ADD ARTICLE TABLE TO DATABASE
ap_content = build_article_directory()
def article_db():

	# Create variables and commands relating to the database table.
	con = sqlite3.connect("206_final_data.db")
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS Articles")
	cur.execute("CREATE TABLE IF NOT EXISTS Articles (art_title TEXT PRIMARY KEY, art_info TEXT, art_url TEXT, art_thumb TEXT)")

	# Populate the table based on the list of Article objects created.
	ap_base = "INSERT OR IGNORE INTO Articles VALUES (?, ?, ?, ?)"
	for ap in ap_content:
		cur.execute(ap_base, ap)

	# Commit this table, and close the whole database.
	con.commit()
	con.close()

# PART FOUR -- PROCESSING / PRINTING

# List the individual pars for the state chosen, and return which one was chosen.
def list_parks(state_abv):
	# Get the parks whose mailing addresses are in the current state.
	parks_in_state = []
	for s in full_np_objects:
		if state_abv in s.state_abvs:
			parks_in_state.append(s)
	print("HERE ARE ALL PARKS WITH ADDRESSES LISTED IN " + state_abv + ":")
	print("WHICH ONE WOULD YOU LIKE TO KNOW MORE ABOUT?")
	num = 1
	# Show all of the options for parks.
	for p in parks_in_state:
		print(str(num) + ". " + p.name)
		num += 1
	choicepark = int(input())
	# Return the correct NationalPark object.
	return parks_in_state[choicepark - 1]

# Guides the user through choosing a state.
def run_parkfinder():
	print("PLEASE ENTER THE TWO-LETTER ABBREVIATION OF THE STATE YOU'D LIKE TO VIEW PARKS FOR.")
	print("IF YOU DO NOT KNOW YOUR STATE'S ABBREVIATION, ENTER \"HELP\" ")
	
	temp_state_dict = sorted(states_dict.items())
	chosen = False

	while (not chosen):
		choice = input()
		# Runs the help option, printing all state abbreviations.
		if (choice == "HELP" or choice == "Help" or choice == "help"):
			for abv, ent in temp_state_dict:
				print(abv + " is " + ent)
		# If the abbreviation is valid, returns that state.
		elif choice in rev_states_dict:
			print("YOU CHOSE " + rev_states_dict[choice])
			return choice
			chosen = True
		# Otherwise, the command must be invalid.
		else:
			print("COMMAND NOT RECOGNIZED")

# Guides the user through choosing and viewing an article
def run_articlefinder():
	# List the available articles, and have the user choose one.
	print("WHICH ARTICLE WOULD YOU LIKE TO SEE?\n")
	art_choice = 1
	ap_too = build_article_directory()
	for ap in ap_too:
		print (str(art_choice) + ". " + ap[0])
		art_choice += 1
	art_sel = int(input())
	print("\nYOU CHOSE: " + ap_content[art_sel - 1][0])
	# Find what the user wants to view.
	print("WOULD YOU LIKE A SYNOPSIS, THE THUMBNAIL, OR THE FULL ARTICLE?\n1. SYNOPSIS\n2. THUMBNAIL\n3. FULL ARTICLE\n")
	synfull = input()
	if (synfull == "1"):
		# Show the synopsis, then show the full article if desired.
		print(ap_content[art_sel - 1][1])
		print("WOULD YOU LIKE TO VIEW THE FULL ARTICLE?\n\n1. YES\n2. NO\n")
		fullthough = input()
		if (fullthough == "1"):
			webbrowser.open_new_tab(ap_content[art_sel - 1][2])
			print("OPENING THE ARTICLE IN YOUR BROWSER...\n")
	elif (synfull == "2"):
		# Show the thumbnail in the default browser., then show the full article if desired.
		webbrowser.open_new_tab(ap_content[art_sel - 1][3])
		print("OPENING THE THUMBNAIL IN YOUR BROWSER...\n")
		print("WOULD YOU LIKE TO VIEW THE FULL ARTICLE?\n\n1. YES\n2. NO\n")
		fullthough = input()
		if (fullthough == "1"):
			webbrowser.open_new_tab(ap_content[art_sel - 1][2])
			print("OPENING THE ARTICLE IN YOUR BROWSER...\n")
	else:
		# Open the article in the default browser.
		webbrowser.open_new_tab(ap_content[art_sel - 1][2])
		print("OPENING THE ARTICLE IN YOUR BROWSER...\n")

# Handles the user's interaction with the program.
def run_program():
	# Prints the initial dialogue.
	print("\n//////////////////////////////")
	print("  WELCOME TO THE PARKFINDER")
	print("//////////////////////////////\n")
	print("WHAT WOULD YOU LIKE TO VIEW?\nPLEASE ENTER THE NUMBER OF THE OPTION YOU'D LIKE\n")
	print("1. PARK INFORMATION")
	print("2. NPS ARTICLES")
	print("3. ALL PARKS' NAMES")
	print("0. NOTHING -- QUIT\n")

	##########

	# Selection of program function -- runs individual functions from here.
	picked = False
	while (not picked):
		opt = input()
		# When 1 is chosen, run the parkfinder set of functions.
		if (opt == "1"):
			state_in = run_parkfinder()
			chosen_park = list_parks(state_in)
			print("\n\n//////////////////////////////\nHERE IS THE INFORMATION FOR THAT PARK.\nYOU CAN READ MORE AT " + chosen_park.park_url + "\n//////////////////////////////\n")
			print(chosen_park)
			picked = True
		# When 2 is chosen, run the articlefinder set of functions.
		elif (opt == "2"):
			run_articlefinder()
			picked = True
		# When 3 is chosen, just print all of the park objects' names.
		elif (opt == "3"):
			for s in full_np_objects:
				print(s.name)
			picked = True
		# When 4 is chosen, escape the while loop.
		elif (opt == "0"):
			picked = True
		# Otherwise, the input must have not been valid.
		else:
			print("COMMAND NOT RECOGNIZED.")

	# Regardless of input, print a thank you message upon exiting.
	print("\nTHANK YOU FOR USING THE PARKFINDER!\n")


# PART FIVE -- RUNNING THE PROGRAM.
# Create the park info and commit it to the database if not done already.
update_db()
# Create the state info and commit it to the database if not done already.
state_db()
# Create the article info and commit it to the database if not done already.
article_db()
# Run the program by handling user input.
run_program()

# Put your tests here, with any edits you now need from when you turned them in with your project plan.

# Test NationalPark member variables
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

# Test NationalPark member functions
class TestParkMembers(unittest.TestCase):
	def test_short_print(self):
		spr_test = NationalPark("https://www.nps.gov/hobe/")
		self.assertEqual(type(spr_test.short_print()), type("Printable string"), "Testing that short_print returns a printable string.")
	def test_short_phone(self):
		sph_test = NationalPark("https://www.nps.gov/hobe/")
		self.assertEqual(type(sph_test.short_phone()), type("Printable string"), "Testing that short_phone returns a printable string.")

# Test Article member variables
class TestArticles(unittest.TestCase):
	def test_article_title(self):
		art_in = ("Example Article Title", "Example Synopsis", "Example URL", "Example Thumb")
		art_test = Article(art_in)
		self.assertEqual(art_test.title, "Example Article Title")
	def test_article_synopsis(self):
		art_in = ("Example Article Title", "Example Synopsis", "Example URL", "Example Thumb")
		art_test = Article(art_in)
		self.assertEqual(art_test.synopsis, "Example Synopsis")
	def test_article_url(self):
		art_in = ("Example Title", "Example Synopsis", "Example URL", "Example Thumb")
		art_test = Article(art_in)
		self.assertEqual(art_test.url, "Example URL")
	def test_article_thumb(self):
		art_in = ("Example Article Title", "Example Synopsis", "Example URL", "Example Thumb")
		art_test = Article(art_in)
		self.assertEqual(art_test.thumb, "Example Thumb")

# Test directory generating functions
class TestDirectories(unittest.TestCase):
	def test_park_directory(self):
		bpd = build_park_directory()
		correct = []
		self.assertEqual(type(bpd), type(correct))
	def test_state_directory(self):
		bsd = build_state_directory()
		correct = []
		self.assertEqual(type(bsd), type(correct))
	def test_article_directory(self):
		bad = build_state_directory()
		correct = []
		self.assertEqual(type(bad), type(correct))
	def test_weather_directory(self):
		bwd = build_weather_directory()
		correct = {}
		self.assertEqual(type(bwd), type(correct))

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)

if __name__ == "__main__":
	unittest.main(verbosity=2)
