import logging, os

DEBUG = False
API_HOST = 'http://localhost:5000/api'
SENSING_DATA_FILE = 'sensingData.txt'

#Loggging Config
logDir = os.path.dirname(__file__)
log_file = os.path.join(logDir,'log','api.log')
log_file_suffix = "%Y-%m-%d"
log_formatter = '% (asctime)'
log_formatter = '%(asctime)s - %(levelname)s - %(message)s'
log_level=logging.INFO