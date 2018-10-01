## The stock tracker object

## There will be three lists:
## A code list that contains all the codes from the raw data files
## A watch list that conatins the stock codes that the user is interested in
## An ignore list that the user specifically does not want to be notified of

## The Tracker object handles the day-to-day management of the data
## It will determine when updates will occur, and handle notifying the user of interesting info
## I imagine it will be possible to have multiple trackers running with different watch lists, but I don't see why this should happen
## Perhaps running this as a singleton would be a good idea

from global_vars import *
import csv
import stock


class Tracker:
	def __init__(self, initial_watch_list):
		self.watch_list = []
		self.WATCH_LIST_FILE = initial_watch_list
		self.is_installed()

	def GetWatchList(self):
		## Loads the watch_list from file

		watch_list = []
		with open(self.WATCH_LIST_FILE,'r') as file:
			data_reader = csv.reader(file)
			watch_list = list(data_reader)

		return watch_list

	def eod_update(self):
		## for each stock, run its update procedure
		pass

	def notify(self):
		## for each stock in the watch list, notify the user of events they are interested in
		pass

	def weekend_update(self):
		## Download the historical data

		pass

	def startup_sequence(self):
		## Things to do when booted
		

		pass

	def is_installed(self):
		## Checks if all the data needed to run properly has been loaded
		## If not, runs the install proceedure

		pass

	def add_stock(self):
		## Procedure to add a new stock to the stock list
		pass

	



