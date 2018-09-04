'''
Author: Roberto Pacheco
Date: August, 29, 2018
Modified: Roberto Pacheco
Last Modified: September, 01, 2018

Description:
Config the Flushing Layer
'''

import logging, os

DEBUG = True
PORT = 5000
URL_PUBLICATION = 'https://sensingbus.gta.ufrj.br/measurements_batch_sec/'
API_HOST = 'http://localhost:5000/api'

QUEUE_TIME = 10
FLUSHING_ID = 1
webapiDir = os.path.dirname(__file__)

#path to certificate e key files
SSL_CERT = os.path.join(webapiDir, 'certificates', 'server.csr')
SSL_KEY = os.path.join(webapiDir, 'certificates', 'server.key')
UPLOAD_PATH = os.path.join(webapiDir, 'app', 'api', 'modules')

#Loggging Config
log_file = os.path.join(webapiDir,'log','api.log')
log_file_suffix = "%Y-%m-%d"
log_formatter = '% (asctime)'
log_formatter = '%(asctime)s - %(levelname)s - %(message)s'
log_level=logging.INFO