import os
import csv
import log
import sys
import pytest
import filecmp

import stock
import installer
import updater
import tracker
import signals

from global_vars import *

import message

TEST_CODE = 'CSL'

class TestSignals(object):

	def test_PeriodHigh(self):

		stk = stock.Stock(TEST_CODE,updater.FromBigCharts)
		sig = signals.Signals()
		high = sig.PeriodHigh(stk, 100)

		assert(high == False)


	def test_PeriodLow(self):

		stk = stock.Stock(TEST_CODE,updater.FromBigCharts)
		sig = signals.Signals()
		Low = sig.PeriodLow(stk, 100)

		assert(Low == False)

	def test_Popup(self):
		stk = stock.Stock(TEST_CODE,updater.FromBigCharts)
		msg = 'testy test\ntesty test'

		message.popupmsg(stk,msg)

