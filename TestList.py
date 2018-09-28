## This file contains all the unit tests to make sure everything works as it is written

import os
import filecmp

import installer

G_ALL_CODES_FILE = 'all_codes.csv'

PATH_FOR_INSTALLER = '/Users/phillipbrown/StockWatch/testing/'
RAW_DATA = PATH_FOR_INSTALLER + 'raw_data/'
STOCK_DATA = PATH_FOR_INSTALLER +'data/'
COMPARISON_FILES_PATH = PATH_FOR_INSTALLER + 'cmp_files/'


COMPARISON_ALL_CODES_FILE =  COMPARISON_FILES_PATH + G_ALL_CODES_FILE
ALL_CODES_FILE = PATH_FOR_INSTALLER + G_ALL_CODES_FILE


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
	## This tests check that the latest codes are retrieved correctly
	## and stored in the correct location
	clear_testing_folder()

	all_codes = []
	with open(self.COMPARISON_ALL_CODES_FILE, 'r') as csvfile:
		codes_reader = csv.reader(csvfile,delimiter=',')
		all_codes = list(codes_reader)

	inst = installer.Installer(PATH_FOR_INSTALLER,RAW_DATA)
	inst.GetInitialCodes()
	assert os.path.isfile(ALL_CODES_FILE)
	assert filecmp.cmp(ALL_CODES_FILE,COMPARISON_ALL_CODES_FILE)
	assert ## assert that the initial codes match the codes in all_codes

def 




def clear_testing_folder():
	os.system('rm ' + PATH_FOR_INSTALLER +'*')
	os.system('rm -rf ' + STOCK_DATA)

