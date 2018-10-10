## The main script for Stockwatch:
## - Starts the tracker and loops
## This script will be daemonised

import tracker
import stock
import updater

import datetime as dt
import time
import sys
#PATH_FOR_INSTALLER = '/Users/Manda/StockWatch/testing/'
PATH_FOR_INSTALLER = '/Users/phillipbrown/StockWatch/testing/'
sys.path.insert(0, PATH_FOR_INSTALLER)
from global_vars import *

WATCH_LIST = APP_PATH + 'cmp_files/watch_list.csv'

## Initialise the tracker
trk = tracker.Tracker(WATCH_LIST)

# ensures that the updates run the first time
checked_date 	= dt.date(2000,1,1) 
dl_checked_date = dt.date(2000,1,1)


while(True):
	date 	= dt.date.today()
	day 	= dt.date.today().weekday()
	hour 	= dt.datetime.now().hour

	if day < 5 and hour > 16 and checked_date < date: # if we're on a weekday after 5pm and we haven't updated already
		## THIS CAN ONLY RUN AFTER GMT -6
		## There is a bug on the BigCharts website where yesterday's data
		## appears as todays data due to time difference.
		trk.EoDUpdate()
		trk.GetSignals()
		checked_date = date
	
	if day == 0 and hour > 14 and dl_checked_date < date:
		trk.UpdateArchive()
		dl_checked_date = date
	
		

	time.sleep(900) # check every 15 minutes




