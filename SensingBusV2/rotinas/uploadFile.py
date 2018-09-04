import sys, requests, config, logging


fileName = input("Insira o nome do arquivo da Coleta\n")
if(fileName == ''):
	'''logging.error("Nao foi inserido nenhum arquivo.")
	sys.exit()'''
	fileName = 'sensingData.txt'

try:
	url = config.API_HOST + '/uploadModules'
	file = {'file': open(fileName,'rb')}
	values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
	r = requests.post(url, files=file, data=values)
	if (r.status_code == 200 or r.status_code == 201):
		logging.info("Sensing Data was inserted successfully")
	else:
		raise Exception("Failed to insert Sensing Data")

except Exception as err:
	logging.error("Routine Failed")
	logging.error(err.args)
	sys.exit()