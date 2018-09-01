'''
Author: Roberto Pacheco
Date: August, 29, 2018
Modified: Roberto Pacheco
Last Modified: August, 29, 2018

Description:
Config the run.py
'''
import logging, os

DEBUG = True
PORT = 5000

#Loggging Config
logDir = os.path.dirname(__file__)
log_file = os.path.join(logDir,'log','api.log')
log_file_suffix = "%Y-%m-%d"
log_formatter = '% (asctime)'
log_formatter = '%(asctime)s - %(levelname)s - %(message)s'
log_level=logging.INFO