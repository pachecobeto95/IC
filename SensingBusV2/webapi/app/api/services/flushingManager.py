from flask import jsonify, current_app as app
import json, requests, time, queue


q = queue.Queue()

def __sendThread(thread_name,q):

	while 1:
		output={}
		output['batches'] = []
		if not q.empty():
			while not q.empty():
				b = q.get()
				if(b is not None):
					output['batches'].append(b)

			time.sleep(30)


def __sendToPublication(payload):
	URL_PUBLICATION = 'https://sensingbus.gta.ufrj.br/measurements_batch_sec/'
	header = {'Content-Type' : 'application/json'}
	r = requests.post(URL_PUBLICATION, data=payload, headers=header)

	return r.status_code

def preProcessing(data):

	q.put(data)
	

	return {"status" : "ok", "msg" : "Dados da Coleta foi recebido"}