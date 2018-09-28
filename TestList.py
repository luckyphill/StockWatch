## This file contains all the unit tests to make sure everything works as it is written

import os

import installer

PATH_FOR_INSTALLER = '/Users/phillipbrown/StockWatch/testing/'
RAW_DATA = PATH_FOR_INSTALLER + 'raw_data/'
STOCK_DATA = PATH_FOR_INSTALLER +'data/'

#==========================================
# Use pytest to test things work correctly
# If you don't have pytest, get it using:
# pip install -U pytest
# and check your install using:
# pytest --version
#==========================================

def testSetInstallerPaths():
	inst = installer.Installer(PATH_FOR_INSTALLER,RAW_DATA)
	assert inst.GetPath() == PATH_FOR_INSTALLER
	assert inst.GetRawPath() == RAW_DATA


def testGetInitialCodes():
	## This test check that the latest codes are retrieved correctly
	clear_testing_folder()

	inst = installer.Installer(PATH_FOR_INSTALLER,RAW_DATA)
	inst.GetInitialCodes()



def clear_testing_folder():
	os.system('rm ' + PATH_FOR_INSTALLER +'*')
	os.system('rm -rf ' + STOCK_DATA)

