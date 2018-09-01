
import sys, requests, config, logging


fileName = input("Insira o nome do arquivo da Coleta\n")
if(fileName == ''):
	fileName = config.SENSING_DATA_FILE


try:
	url = config.API_HOST + '/sensingData'
	file = open(fileName, 'r')
	header = {'Content-Type' : 'application/x-www-form-urlencoded'}
	#r = requests.post(url, data=file.read())
	r = requests.post(url, data=file.read(), headers=header)
	if (r.status_code == 200 or r.status_code == 201):
		logging.info("Sensing Data was inserted successfully")
	else:
		raise Exception("Failed to insert Sensing Data")

except Exception as err:
	logging.error("Routine Failed")
	logging.error(err.args)
	sys.exit()