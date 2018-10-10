


class Signals:

	def PeriodHigh(self, stock, ndays):
		## Returns true if the current close price is the highest
		## in the given number of days.
		isHighest = True

		data = stock.GetStockData(ndays)
		close_prices = data[:][4]
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

		data = stock.GetStockData(ndays)
		close_prices = data[:][4]
		last_close = close_prices[-1]
		for price in reversed(close_prices[:-1]):
			if price <= last_close:
				isLowest = False
				break

		return isLowest