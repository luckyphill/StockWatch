
import sys
import stock

from global_vars import *


class Signals:

	def PeriodHigh(self, stock, ndays):
		## Returns true if the current close price is the highest
		## in the given number of days.
		isHighest = True

		#logger = logging.getLogger(SIGLOG)
		#logger.info("Checking for period high for %s", stock.code)

		data = stock.GetStockData(ndays)
		close_prices = [line[4] for line in data]
		last_close = close_prices[-1]

		for price in reversed(close_prices[:-1]):
			if price >= last_close:
				isHighest = False
				break

		return isHighest

	def PeriodLow(self, stock, ndays):
		## Returns true if the current close price is the Lowest
		## in the given number of days.
		isLowest = True

		#logger = logging.getLogger(SIGLOG)
		#logger.info("Checking for period low for %s", stock.code)

		data = stock.GetStockData(ndays)
		close_prices = [line[4] for line in data]
		last_close = close_prices[-1]

		for price in reversed(close_prices[:-1]):
			if price <= last_close:
				isLowest = False
				break

		return isLowest

	def CheckForSignals(self, stock):
		## Runs through the signals and prepares the messages
		logger = logging.getLogger(SIGLOG)
		sigs = []
		## Do we have a n-period break out?
		if self.PeriodHigh(stock,150):
			message = stock.code + " has closed higher than the previous 150 days of trading"
			logger.info("%s has closed higher than the previous 150 days of trading", stock.code)
			sigs.append(message)

		if self.PeriodLow(stock,150):
			message = stock.code + " has closed lower than the previous 150 days of trading"
			logger.info("%s has closed lower than the previous 150 days of trading", stock.code)
			sigs.append(message)

		return sigs