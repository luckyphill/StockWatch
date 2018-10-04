import logging
import logging.handlers

## Setup the logger so that it can be used in the global_vars file
## This will make it easier and more clean to have all modules log to the same file
def setup_custom_logger(name,path):

	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)
	if not len(logger.handlers):
		formatter = logging.Formatter(fmt='%(asctime)s - %(module)s - %(message)s')
		handler = logging.handlers.RotatingFileHandler(path,mode='a', maxBytes=1048576, backupCount=1)
		handler.setFormatter(formatter)
		logger.addHandler(handler)

	return logger
