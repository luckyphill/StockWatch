## An installer function
## Not sure the best way to do this, but will start off as an object

## In order to install, we need the data in a known location in a known format
## The assumed format will be that which comes from www.asxhistoricaldata.com
## Each trading day has a file name YYYYMMDD.txt
## In that file we have for each stock, the code price data, volume data and other stuff
## for that given day
## The data will be processed to be in the form of time series data for each stock
## This will be found in a folder structure StockWatch/data/CODE/time_series.txt
## Firstly this folder structure will be created - this means we need a list of codes
## Secondly, the data will be cleaned and placed in the appropriate file
## Thirdly, all the file paths for each stock, a watch list etc. will be written to a 
## data file which will serve as global variable holder type thing
## The installer will only run if this file does not exist, otherwise, things will be
## handled by the Tracker object

class Installer:
	def __init__(self,path):

		pass

	def install(self):
		## Performs the installation
		pass

	def write_installation_file(self):
		## Writes a file that will be used to track all the information about
		pass
