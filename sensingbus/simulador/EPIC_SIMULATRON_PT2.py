#Authors:Roberto Pacheco
#Universidade do Estado do Rio de Janeiro
#Departamento de Eletronica e Telecomunicacoes (DETEL)
#Project: SensingBus
#Subject: Simulate the Comunication between Cloud and Fog (PT2). Simulate the compression.

import random
import time
import datetime
import json
import requests
import zlib
import threading, Queue

random.seed(time.time())
q = Queue.Queue()
QUEUE_TIME = 30
FOG_INICIO = 0
FOG_FIM = 6000
FOG_STEP = 500
FileName = 'size_dados_ate_'
class Data:#create message's load
    def __init__(self):
        self.datetime = datetime.datetime.now().strftime('%d%m%y%H%M%S')
        self.latitude = random.uniform(-22.3,-22.6)
        self.longitude = random.uniform(-43.3,-43.6)
        self.light = random.randint (997,999)
        self.temperature = random.uniform(20.0, 50.0)
        self.humidity = random.uniform (28.0, 31.0)
        self.rain = random.randint (774, 781)
        self.data = str(self.datetime) + '00' + ',' + str(self.latitude) + ',' + str(self.longitude) + ',' + str(self.light) + ',' + str(self.temperature) + ',' + str(self.humidity) + ',' + str(self.rain)

def generateData (max_gathering):
    dataList = []

    for line in range (0, max_gathering):
        dataList.append(Data().data)

    return dataList


def createMessage(sensing_node, data):#creates the diccionary to the message
    message = {}

    message["node_id"] = sensing_node
    message["type"] = 'data'
    message["header"] = "datetime,lat,lng,light,temperature,humidity,rain"
    message["load"] = data

    return message

def worker(thread_name,q):#Queue Accumulation. Wait the "QUEUE_TIME" receiving data to send it later 
	
	while 1:
		datafinal = []
		if not q.empty():
			while not q.empty():
				data = q.get()
				if (data is not None):
					datafinal.append(data)

			time.sleep(QUEUE_TIME)

for nr_fog in range(FOG_INICIO, FOG_FIM, FOG_STEP):
	FileTemp = open('test_files/' + str(FileName) + str(id_fog_node) + '.tmp', 'r')
	size_msg_list = []
	media_size_msg_list = 0
	for line in FileTemp.readlines()
		line_list = line.split()
		size_msg_list.append(line_list[4])
		
	media_size_msg_list = sum(float(size_msg_list)) / len(size_msg_list)
	t = threading.Thread( target = send_thread, args=('alt',q))
	t.daemon = True
	t.start()
	data = generateData (media_size_msg_list)
	q.put(createMessage(media_size_msg_list, data))
t.join()














