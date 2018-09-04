from flask import jsonify, session, current_app as app
import json, requests, time, queue, config, datetime, logging


q = queue.Queue()

def __sendThread(thread_name,q):

	while 1:
		output={}
		output['batches'] = []
		output['received'] = []
		output['flushing_id'] = config.FLUSHING_ID
		if not q.empty():
			while not q.empty():
				b = q.get()
				if(b is not None):
					output['header'] = b['header']
					output['sensing_id'] = b['node_id']
					output['type'] = b['type']
					output['batches'].append(b['load'])
					output['received'].append(b['received'])
			#sendToPublication(output)

def sendToPublication(payload):
	try:
		header = {'Content-Type' : 'application/json'}
		return __sendData(config.URL_PUBLICATION, payload, header, config.SSL_CERT)
	except Exception as err:
		return {'status':'error', 'msg':err.args}
	


def __sendData(url, payload, header, cert=None):
	try:
		r = requests.post(url, data=payload, headers=header, verify=cert)
	except Exception as e:
		logging.error(e, exc_info=True)


def preProcessing(data):
	try:
		data['received'] = str(datetime.datetime.now())
		q.put(data)

		if('output' in session):
			output = session['output']
		return {"status" : "ok", "msg" : "Dados da Coleta foi recebido"}

	except Exception as e:
		logging.error(e, exc_info=True)
		return {'status':'error','msg':'Não foi possível gerar os dados de risco.'}
