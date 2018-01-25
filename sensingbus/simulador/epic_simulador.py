'''Author:Roberto Pacheco
Universidade do Estado do Rio de Janeiro
Departamento de Eletronica e Telecomunicacoes (DETEL)
Project: SensingBus
Subject: Simulate the Comunication between Cloud and Fog (PT2). Simulate the compression.
'''

import random
import time
import datetime
import json
import requests
import zlib
import threading, Queue
import sys
import math
from geopy.distance import vincenty
import time, datetime
import MySQLdb

RANGE_FOG = 300
size_msg_list = []
random.seed(time.time())
q = Queue.Queue()
QUEUE_TIME = 30
FOG_INICIO = 1
FOG_FIM = 6101
FOG_STEP = 100
COMPRESSION_LEVEL=1
WORD_SIZE_BITS=-15
MAX_MEASURES=100
MEM_LEVEL=9
STOP_ID = 1
OFFSET=1
conexoes_bus = []
conexoes_fog = []
cont = 1

def generateData (max_gathering):

	
	dataList = []

	for line in range (0, max_gathering):
		dataList.append(Data().data)

	return dataList


def createMessage(sensing_node, data):
	''' This function creates the diccionary to the message.

		arg1: a float to identify the fog node.

		arg2: a list of data to build a complete message.
	 '''

	message = {}
	message["node_id"] = sensing_node
	message["type"] = 'data'
	message["header"] = "datetime,lat,lng,light,temperature,humidity,rain"
	message["load"] = data

	return message


def worker(thread_name,q):

	''' This function is a Queue Accumulation. It waits the "QUEUE_TIME" receiving data to send it later.

		arg1: a string tha thread name.

		arg2: a queue to receive the data to be accumulated.
	'''

	while 1:
		datafinal = []
		time_acc = 0
		while time_acc <= QUEUE_TIME:
			if not q.empty():
				while not q.empty():
					data = q.get()
					if (data is not None):
						datafinal.append(data)
				fog = Fog(fog_node)
				fog.compression(datafinal)
				time_acc = time_acc + 1

class Data(object):

	''' This class creates a message's load. '''

	def __init__(self):
		self.datetime = datetime.datetime.now().strftime('%d%m%y%H%M%S')
		self.latitude = random.uniform(-22.3,-22.6)
		self.longitude = random.uniform(-43.3,-43.6)
		self.light = random.randint (997,999)
		self.temperature = random.uniform(20.0, 50.0)
		self.humidity = random.uniform (28.0, 31.0)
		self.rain = random.randint (774, 781)
		self.data = str(self.datetime) + '00' + ',' + str(self.latitude) + ',' + str(self.longitude) + ',' + str(self.light) + ',' + str(self.temperature) + ',' + str(self.humidity) + ',' + str(self.rain)



class Fog(object):

	def __init__(self, fog_node):
		
		self.fog_node = fog_node.split()
		self.id = self.fog_node[0]
		self.coord_fog = (self.fog_node[1], self.fog_node[2])
		
	def compression(self, data):

		''' This function compresses the data and it writes the data in a file.

			arg1: a list of the data to be compressed

		 '''
		
		compressed_data = zlib.compressobj(COMPRESSION_LEVEL, zlib.DEFLATED, WORD_SIZE_BITS, MEM_LEVEL, zlib.Z_HUFFMAN_ONLY)
		message_text = json.dumps(data)
		size_before_compression = float(sys.getsizeof(message_text))
		messageText = message_text.encode('utf-8').encode('zlib_codec')
		t0 = time.time()
		messageText = compressed_data.compress(messageText)
		messageText += compressed_data.flush()
		tf = time.time()
		sife_after_compression = float(sys.getsizeof(messageText))
		delta_t = tf - t0
		compression_ratio = sife_after_compression / size_before_compression
		compression_gain = 100 * (math.log(size_before_compression / sife_after_compression))

class Bus(object):

	def __init__(self, bus_node):
		self.bus_node = bus_node.split()
		self.day = self.bus_node[1]
		self.hour = self.bus_node[2]
		self.id = self.bus_node[3]
		self.coord_bus = (self.bus_node[4], self.bus_node[5])
		
	def a(self):

		print 'oi'
		
class Simulador(Bus, Fog):

	def __init__(self, fog_node, bus_node):

		Bus.__init__(self, bus_node)
		Fog.__init__(self, fog_node)
		
		
	def conecta(self):

		distance = vincenty(self.coord_fog, self.coord_bus).meters
		
		if (distance <= RANGE_FOG):
			conexoes_bus.append(self.bus_node)
			conexoes_fog.append(self.fog_node)

			#size_msg = procurar_ultima_conexao(conexoes_bus)

			t = threading.Thread( target = worker, args=('alt',q))
			t.daemon = True
			t.start()
			data = generateData(50)
			q.put(createMessage(50, data))
			

def procurar_ultima_conexao():

			
	return size_msg
		
if __name__ == "__main__":
	
	
	FileBus = open("./sql_sbrc2018_Buses.tmp", 'r')
	
	for bus_node in FileBus.readlines():
		FileFog = open("./sql_sbrc2018_Stops.tmp", 'r')
		bus = Bus(bus_node)
		for fog_node in FileFog.readlines():
			fog = Fog(fog_node)
			s = Simulador(fog_node, bus_node)
			evento = s.conecta()
			
	


		FileFog.close()

	FileBus.close()












