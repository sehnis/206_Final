PARKFINDER
==========

SI206 Final Project by Sam Ehnis-Clark [sehnis]
-----------------------------------------------

General Information
-------------------

Option 1 (Though the printed information is varied from the spec)

The program has three functionalities:
	- It can show users park info, based on a chosen state and park.
	- It can show users articles, and open them in their browser.
	- It can list all of the parks on the NPS website.
It's main purpose is the first option, which guides them through choosing a park
and presents information on many aspects of the park, such as contact info, weather,
and the type of park that it is.

The program is contained entirely within the data_access file, but imports a number of libraries:
	- from bs4 import BeautifulSoup (HTML parsing)
	- codecs (UTF-8 compatibility)
	- collections (Data processing)
	- json (HTML parsing)
	- re (Data processing, specifically on addresses)
	- requests (HTML parsing)
	- sqlite3 (Database storage)
	- sys (Permissions)
	- unittest (Testing)
	- webbrowser (Opening articles)

Usage: python 206_data_access.py

The program prompts the user for input on which functionality to use.
Several options lead to further choices, as the user will see.
The tree of choices is as follows:

1. See park information
	1. Enter state abbreviation
		1 - N. Choose park from list of all parks in state
			* Data is printed about the desired park
	2. See all abbreviations
		* State abbreviations are printed, user is reprompted for input
2. See article information
	1 - N. Choose article from list of all articles
		1. View the synopsys
			* Synopsis is printed 
			1. View the full article
				* Article is opened in the default browser
			2. Do not view the full article
				* Program exits
		2. View the thumbnail
			* Thumbnail is opened in the default browser
			1. View the full article
				* Article is opened in the default browser
			2. Do not view the full article
				* Program exits
		3. View the article
			* Article is opened in the default browser
3. Print all parks' names
	* All park names are printed
0. Exit
	* Program exits with a "thank you" message


BeautifulSoup/Database Functions
--------------------------------
Name:		build_state_directory()
Purpose:	Creates a list of the state URLs found on the NPS website.
Arguments:	None.
Return Type:	List of strings.
Return Info:	URLS, formatted like https://www.nps.gov/state/ak/index.htm
--------------------------------
Name:		build_park_directory()
Purpose:	Uses state URLs to get all park URLs.
Arguments:	None, but calls build_state_directory() internally.
Return Type:	List of strings.
Return Info:	URLS, formatted like https://www.nps.gov/frst/
--------------------------------
Name:		update_db()
Purpose:	Commits park data to 206_final_data.db
Arguments:	None.
Return Type:	None.
Return Info:	N/A.
--------------------------------
Name:		build_article_directory()
Purpose:	Gets the information of the articles on the NPS index page.
Arguments:	None.
Return Type:	List of tuples of strings.
Return Info:	Tuples contain the articles name, summary, thumbnail URL, and URL.
--------------------------------
Name:		article_db()
Purpose:	Commits article data to 206_final_data.db
Arguments:	None.
Return Type:	None.
Return Info:	N/A.
--------------------------------
Name:		build_weather_directory()
Purpose:	Gets weather information for the states.
Arguments:	None.
Return Type:	Dictionary of state names and temperatures (F and C)
Return Info:	The key is the full name of the state, and the temperatures are in a tuple.
--------------------------------
Name:		state_db()
Purpose:	Commits state/weather data to 206_final_data.db
Arguments:	None.
Return Type:	None.
Return Info:	N/A.
--------------------------------


NationalPark Class 
------------------
Variables
---------
park_url	URL used to create park, to reference later.
name		Name of the park.
park_type	What kind of park it is (National Monument, etc.)
states		Which states the park spans.
address		The official address of the park.
phone		The phone number for the park.
has_phone	Whether or not a phone number is listed on the page.
planning	Planning/ammenity information supplied by the website.
state_abvs	List of state abbreviations listed in the address

Methods
-------
Name:		__init__(url)
Purpose:	Initializes a NationalPark object from the park's URL, with BeautifulSoup.
Arguments:	1 string, a URL.
Return Type:	None.
Return Info:	The created NationalPark object has 9 variables, as mentioned above.
------------------
Name:		__str__()
Purpose:	Prints a full description of the park for the user to view.
Arguments:	None.
Return Type:	None, but prints to the console.
Return Info:	Lists url, name, type, address, phone, temperatures, and description.
------------------
Name:		short_print()
Purpose:	Gives a shortened description of the park.
Arguments:	None.
Return Type:	String
Return Info:	Lists only the name and the address, to be printed.
------------------
Name:		short_phone()
Purpose:	Gives only the park's phone number, or URL if not found.
Arguments:	None.
Return Type:	String
Return Info:	Lists the park's phone number or URL, with a helpful message.
------------------


Article Class 
-------------
Variables
---------
title		Title of the article.
synopsis	The synopsis given below the article's thumbnail
url		URL of the article
thumb		Thumbnail URL for the article

Methods
-------
Name:		__init__(art_input)
Purpose:	Initializes a Article object from a tuple of BeautiulSoup data
Note:		Handled within create_article_directory, which uses article URLs
Arguments:	1 tuple of 4 strings
Return Type:	None.
Return Info:	The created Article object has 4 variables, as mentioned above.
-------------


Lookup/User Functions
---------------------
Name:		list_parks(state_abv)
Purpose:	Prints the parks in a certain state, and returns the chosen park.
Arguments:	1 string, the state's abbreviation.
Return Type:	NationalPark
Return Info:	The NationalPark that the user designated, from the full list.
---------------------
Name:		run_parkfinder()
Purpose:	Has the user choose their desired state, or see all state options.
Arguments:	None.
Return Type:	String
Return Info:	The two-letter state abbreviation chosen by the user.
---------------------
Name:		run_articlefinder()
Purpose:	Has the user choose an article, and view aspects of it.
Arguments:	None.
Return Type:	None, but prints to the console and/or opens a browser tab.
Return Info:	Opens the thumbnail/article in the user's default browser.
---------------------
Name:		run_program()
Purpose:	Prints the initial message, and gets the user's decision.
Arguments:	None.
Return Type:	None, but prints to the console.
Return Info:	Prints a "thank you" message at the end, regardless of option.


Database Content
----------------
Table One: Articles
Column Name   	|   Column Type	|   Column Content
art_title	|   string	|   Lists the article's title
art_info	|   string	|   Lists the article's synopsis
art_url		|   string	|   Lists the article's URL
art_thumb	|   string	|   Lists the URL of the article's thumbnail
----------------
Table Two: Parks
Column Name   	|   Column Type	|   Column Content
park_name	|   string	|   Lists the park's name
park_info	|   string	|   Lists the park's contact info as a synopsis
park_url	|   string	|   Lists the park's URL
park_phone	|   string	|   Lists the park's phone number
park_states	|   string	|   Lists the states that the park is in
park_address	|   string	|   Lists the park's mailing address
----------------
Table Three: States
Column Name   	|   Column Type	|   Column Content
state_name	|   string	|   Lists the state's full name
state_abv	|   string	|   Lists the state's abbreviation
weather_degf	|   string	|   Lists the temperature in fahrenheit
weather_degc	|   string	|   Lists the temperature in celsius


Data Manipulation Questions
---------------------------
What else does the code do?
	- Allows for the user to choose what information they see of all this.
How is it useful?
	- Gives a practical application to the collected data: researching parks relevant to the user.
What will it show you?
	- Depends on the user's choice; it will show park info, articles, or general park listings.
What should a user expect?
	- To find parks in their area, and get a good deal of information about them.


Why I Chose This
----------------

I consider this to be a blend of Options 1 and 3 -- when I started parsing through all of the data that this program was generating, I thought it would be useful to have it return a consise amount of facts about each of the parks in a practical way that gave the user information relevant to them. As such, it expounds upon the Option 1 concept of using National Parks and presents the user with a varied yet very practical set of park/article information.


Extra Notes
-----------

To handle the dilemma of parks spanning multiple states, a park is only listed as being in a state if its mailing address is listed in that state.

Hohokam Pima is "not open to the public," and its page is inaccessible.
It is listed in the database and printed list as [Unnamed Park], and its variables are all placeholders.

Placeholder states ("[UNKNOWN STATE]") have the two-letter abbreviation UK in the database.

In order to show the full program output, only some of the test results are shown. Despite this, all 18 tests pass, as running the program will show.

See the submitted .zip for screenshots of the code running in all 3 modes, as well as proof of commits.


SI 206 Information
------------------
Lines on which each of your data gathering functions begin: 56, 88, 131, 206
Lines on which your class definitions begin: 181, 359
Line where your database is created in the program: 305
Line of code that load data into your database: 193, 347, 449
Lines of code (approx) where your data processing code occurs - where in the file can we see all the processing techniques you used? 108-110, 147-165, 223
Lines of code that generate the output. 458-587

