## The stock object
## Should do all the handling of actual stock data

from global_vars import *
logger = logging.getLogger(LOG)
print DATA_PATH
try:
	TIME_SERIES_FILE_NAME
except:
	logger.info("It's not there")

class Stock:
	def __init__(self, code):
		self.code = code
		self.DIRECTORY = DATA_PATH + code +'/'
		self.DATA_FILE = self.DIRECTORY + TIME_SERIES_FILE_NAME
		## Declaring the object

	def GetDataFile():
		return self.DATA_FILE

	def eod_update(self):
		## Manages all the updating procedures
		pass

	def get_latest_price(self):
		## Accesses the designated website to get the end of day data

		pass

	def initialise_stock(self):
		## Used when there is only raw data

		pass