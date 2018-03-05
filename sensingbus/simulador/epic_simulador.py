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
#Queue = [60, 1800, 3600, 43200, 86400]
Queue = [43200]
QUEUE_TIME = 1800
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
				#fog = Fog(fog_node)
				#fog.compression(datafinal)
				print datafinal
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
		#print 'a fog analisada' + str(self.fog_node)
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
		return compression_ratio, compression_gain, delta_t

	def procura_conexao_fog(self, QUEUE_TIME):
		FileTemp = open("diffhour2.tmp", 'r')
		conexoes_fog = []
		cont = 0
		i = 0
		list_diffhour = []
		
		for conexao in FileTemp.readlines():

			line = conexao.split()
			
			
			distance = vincenty(self.coord_fog, (line[4], line[5])).meters
			
	
			if ( distance <= RANGE_FOG ):	
				conexoes_fog.append(line)
				
		for line1 in conexoes_fog:
			#print 'posicao ref' + str(conexoes_fog[cont])
			for line_conexoes_fog in conexoes_fog:
				#print 'posicao conferida'+ str(line_conexoes_fog)
				#time.sleep(5)
				date1 = float(datetime.datetime.strptime(str(line1[1]) + ' ' +str(line1[2]), '%Y-%m-%d %H:%M:%S').strftime("%s"))
				date2 = float(datetime.datetime.strptime(str(line_conexoes_fog[1]) + ' ' +str(line_conexoes_fog[2]), '%Y-%m-%d %H:%M:%S').strftime("%s"))
				diff_hour = abs(date2 - date1)
				#print 'diferenca tempo calculada' + str(diff_hour)	
				i = i + 1

					
				if ( diff_hour < QUEUE_TIME and int(diff_hour) != 0):
					list_diffhour.append(float(line_conexoes_fog[6]))
					print list_diffhour
					
						
							
				elif (int(diff_hour) != 0):
					data = generateData(int(float(conexoes_fog[cont][6])))
					compression(createMessage(int(float(conexoes_fog[cont][6])), data), QUEUE_TIME)
					#print conexoes_fog[cont][6]
							
		
			if (len(list_diffhour) > 0):
					
				data = generateData(int(sum(list_diffhour)))
				compression(createMessage(int(sum(list_diffhour)), data), QUEUE_TIME)

			#cont = cont + 1
			list_diffhour = []

		
			
				
		FileTemp.close()

def compression(data, QUEUE_TIME):

		''' This function compresses the data and it writes the data in a file.

			arg1: a list of the data to be compressed

		 '''
		arq_compressed = open('compressed_data_' + str(QUEUE_TIME) + '.tmp', 'a')
		compressed_data = zlib.compressobj(COMPRESSION_LEVEL, zlib.DEFLATED, WORD_SIZE_BITS, MEM_LEVEL, zlib.Z_HUFFMAN_ONLY)
		message_text = json.dumps(data)
		#print 'TEMPO DA FILA DE ACUMULACAO ' + str(QUEUE_TIME)
		size_before_compression = float(sys.getsizeof(message_text))
		#print size_before_compression
		#time.sleep(3)
		messageText = message_text.encode('utf-8').encode('zlib_codec')
		t0 = time.time()
		messageText = compressed_data.compress(messageText)
		messageText += compressed_data.flush()
		tf = time.time()
		sife_after_compression = float(sys.getsizeof(messageText))
		#print sife_after_compression 
		delta_t = tf - t0
		compression_ratio = sife_after_compression / size_before_compression
		compression_gain = 100 * (math.log(size_before_compression / sife_after_compression))
		#print compression_gain
		
		arq_compressed.write(str(compression_gain) + " " + str(compression_ratio) + " " + str(delta_t) + '\n')
		arq_compressed.close()
		

		

class Bus(object):

	def __init__(self, bus_node):
		self.bus_node = bus_node.split()
		self.day = self.bus_node[1]
		self.hour = self.bus_node[2]
		self.id = self.bus_node[3]
		self.coord_bus = (self.bus_node[4], self.bus_node[5])
		
	
		
class Simulador(Bus, Fog):

	def __init__(self):

		Bus.__init__(self, bus_node)
		Fog.__init__(self, fog_node)
		
		
	def conecta(self):
		''' calcula a distancia para verificar se ha conexao '''
		distance = vincenty(self.coord_fog, self.coord_bus).meters
	
		if (distance <= RANGE_FOG):
			''' se houver conexao, vai procurar a ultima vez que o aquele onibus teve um contato com uma fog'''	
			procurar_ultima_conexao(self.bus_node)
				

def procurar_ultima_conexao(bus_node):

	if (len(bus_connection) <= 1):
		global cont
		cont = 1
		'''armazena os onibus que tiverem conexao '''
		bus_connection.append(bus_node)
			
		
	if (len (bus_connection) > 1):
		
		if (bus_connection[cont] != bus_node):
			''' armazena os onibus que houver contato '''
			bus_connection.append(bus_node)
			
			if (bus_connection[cont][3] == bus_connection[cont - 1][3]):

				last_connection = bus_connection[cont]
				date1 = float(datetime.datetime.strptime(str(bus_connection[cont][1]) + ' ' +str(bus_connection[cont][2]), '%Y-%m-%d %H:%M:%S').strftime("%s"))
				date2 = float(datetime.datetime.strptime(str(bus_connection[cont - 1][1]) + ' ' +str(bus_connection[cont - 1][2]), '%Y-%m-%d %H:%M:%S').strftime("%s"))
				'''calcula a diferenca de tempo entre ultimas conexoes do onibus '''
				diffhour = abs(date2 - date1)

				if (diffhour != 0):
					'''escreve no arquivo a diferenca de tempo se a diferenca de tempo nao for zero '''
					FileTemp = open("diffhour2.tmp", 'a')
					FileTemp.write(str(last_connection[0]) + ' '  + str(last_connection[1]) + ' ' + str(last_connection[2]) + ' ' + str(last_connection[3]) + ' ' + str(last_connection[4]) + ' ' + str(last_connection[5]) + ' '+ str(diffhour)  + '\n')
					FileTemp.close()
					
				#return diffhour

			else:
				global bus_connection
				bus_connection = []
					
			cont = cont + 1
	
	
		
if __name__ == "__main__":
	
	#for q in Queue:
	FileBus = open("./sql_sbrc2018_Buses.tmp", 'r')
	bus_connection = []
	#FileTemp = open("./sql_sbrc2018_Stops.tmp", 'r')

		#for fog_node1 in FileTemp.readlines():

			#fog_vision = Fog(fog_node1)

	for bus_node in FileBus.readlines():
		'''le cada linha do arquivo como se acompanhando cada onibus pelo seu percurso '''
		FileFog = open("./sql_sbrc2018_Stops.tmp", 'r')
		bus = Bus(bus_node)
		
		for fog_node in FileFog.readlines():
			''' inicia cada fog do arquivo '''
			fog = Fog(fog_node)
			'''inicia o simulador para verificar se ha conexao'''
			s = Simulador()
			
			evento = s.conecta()

		FileFog.close()

			#fog_vision.procura_conexao_fog(q)
	FileBus.close()

	FileTemp.close()











