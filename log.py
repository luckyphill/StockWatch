import logging
import logging.handlers

## UNSOLVED ISSUE: The FileHandler doesn't recognise the absolute path
## It works when the relative path is given, and it works with the relative path
## when it's handeled directly by Installer.py but not in here...

def setup_custom_logger(name,path):

	formatter = logging.Formatter(fmt='%(asctime)s - %(module)s - %(message)s')
	handler = logging.handlers.RotatingFileHandler(path,mode='a', maxBytes=1048576, backupCount=1)
	handler.setFormatter(formatter)

	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)
	logger.addHandler(handler)

	return logger
