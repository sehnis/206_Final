## Your name: Sam Ehnis-Clark
## The option you've chosen:

	#1 -- National Parks

# Put import statements you expect to need here!

	# Getting Data
from bs4 import BeautifulSoup
import json
import requests
	# Processing Data
import collections
import re
import sqlite3
	# Testing
import unittest

# Write your test cases here.

# Testing that the variables used are correctly created, and have the right type.
class TestParkVariables(unittest.TestCase):
	def test_park_name(self):
		name_test = NationalPark(soup_data)
		self.assertEqual(type(name_test.name), type("Alagnak"), "Testing that the park's name is correctly created as a string.")
	def test_park_location(self):
		location_test = NationalPark(soup_data)
		self.assertEqual(type(location_test.location), type("King Salmon, AK"), "Testing that the park's location is correctly created as a string.")
	def test_park_type(self):
		type_test = NationalPark(soup_data)
		self.assertEqual(type(type_test.type), type("Wild River"), "Testing that the park's type is correctly created as a string.")
	def test_park_accessibility(self):
		access_test = NationalPark(soup_data)
		self.assertEqual(type(access_test.access), type([]), "Testing that the park's accessibility information is correctly created as a list.")
	def test_park_url(self):
		url_test = NationalPark(soup_data)
		self.assertEqual(type(url_test.url), type("https://www.nps.gov/alag/"), "Testing that the park's url is correctly created as a string.")
	def test_park_info(self):
		info_test = NationalPark(soup_data)
		self.assertEqual(type(info_test.hasInfo), type(True), "Testing that the park's info status is correctly created as a bool.")

# Testing that (tentative) member functions correctly relay information.
class TestParkMembers(unittest.TestCase):
	def test_forecast(self):
		park_test = NationalPark(soup_data)
		forecast_test = park_test.get_forecast()
		self.assertEqual(type(forecast_test), type("75 degrees, Partly Cloudy"), "Testing that the forecast is returned as a string.")
	def test_all_urls(self):
		park_test = NationalPark(soup_data)
		all_urls = park_test.get_urls()
		self.assertEqual(type(all_urls), type([]), "Testing that the urls are returned as a list.")
		self.assertTrue(len(all_urls) > 1, "Each page has 2 subpages -- this list should have at least 2 urls each.")
	def test_states(self):
		park_test = NationalPark(soup_data)
		all_states = park_test.get_applicable_states()
		self.assertEqual(type(all_states), type([]), "Testing that the states are returned as a list.")
		self.assertEqual(type(all_states[0]), type("MI"), "Testing that the list is a list of strings.")

# Testing that article variables are correct.
class TestArticleVariables(unittest.TestCase):
	def test_article_name(self):
		name_test = Article(soup_data)
		self.assertEqual(type(name_test.art_name), type("Bear Safety"), "Testing that the articles's name is correctly created as a string.")
	def test_article_url(self):
		url_test = Article(soup_data)
		self.assertEqual(type(url_test.art_url), type("https://www.nps.gov/alag/planyourvisit/bearsafety.htm"), "Testing that the articles's url is correctly created as a string.")
	def test_article_content(self):
		content_test = Article(soup_data)
		self.assertEqual(type(content_test.art_content), type("Lorem ipsum dolor set amet"), "Testing that the articles's content is correctly created as a string.")
	
## Remember to invoke all your tests...

if __name__ == "__main__":
	unittest.main(verbosity=2)