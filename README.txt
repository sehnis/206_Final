*PARKFINDER*
===================

*SI206 Final Project by Sam Ehnis-Clark [sehnis]*
-------------------------------------------------

Usage
-----
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
	1. Choose article from list of all articles
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
Return Type:	List of tuples of strings
Return Info:	Tuples contain state abbreviation, fahrenheit temp, and celcius temp.
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
Return Info:	Lists url, name, type, address, phone, and description.
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
