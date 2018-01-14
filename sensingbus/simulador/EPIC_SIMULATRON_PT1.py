#Authors:Roberto Pacheco
# Universidade do Estado do Rio de Janeiro
#Departamento de Eletronica e Telecomunicacoes (DETEL)
#Project: SensingBus
#Subject: Simulate the Comunication between Cloud and Fog (Pt1). Simulate the connection between fog and buses



#import simulador
from geopy.distance import vincenty
#import threading, Queue
import time, datetime
import MySQLdb
def sql_sbrc2018 (table): #connect to the database

	connection = MySQLdb.connect('localhost', 'root', '2904pacheco', 'sbrc2018')
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM sbrc2018." + str(table))
	return cursor.fetchall()
def acc_data_fogs(inicio, fim, step, filenamein, filenameout): #accumulates data of each fog until the number of the fogs installed.
	i = 1
	for nr_fog in range(inicio, fim, step):
		FileTemp2 = open('test_files/' + str(filenameout) + str(nr_fog) + '.tmp', 'a')
		while i <= fog_node: 

			FileTemp = open('test_files/' + str(filenamein) + str(i) + '.tmp', 'r')
			for line in FileTemp.readlines():
				FileTemp2.write(str(i) + ' ' + str(line) + '\n')
			
			i = i + 1
			FileTemp.close()
		FileTemp2.close()	
def organizando_dados_nr_conexoes(inicio, fim, step, filenamein, filenameout): #order the data from "nr_conexoes_ate" files by the hour of connection.

	for nr_fog in range(inicio, fim, step):
		nr_conexoes_ate = open('test_files/' + str(filenamein) + str(nr_fog) + '.tmp', 'r')
		arq_dados_organizados = open('test_files/' + str(filenameout) + str(nr_fog) + '.tmp', 'a')	
		for line nr_conexoes_ate.readlines():

			line_list = line.split()
			ah.append(line_list)

		ordem_bus = sorted(ah, key=lambda ah:ah[4])

		for line in ordem_bus:
			id_node = line[0]
			nr_unknown = line[1]
			day = line[2]
			hour = line[3]
			identification = line[4]
			coord = line[5], line[6]
			arq_dados_organizados.write(str(id_node) + ' ' + str(nr_unknown) + ' ' + str(day) + ' ' + str(hour) + ' ' + str(identification) + ' ' + str(line[5]) + str(line[6]) + '\n')
		arq_dados_organizados.close()
		nr_conexoes_ate.close()		

def size_msg_entre_fog(inicio, fim, step, filenamein, filenameout): #calcula a diferenca do tempo de conexao entre as fogs para saber o tamanho da mensagem para a fog seguinte.

	for nr_fog in range(inicio, fim, step):
		arq_dados_organizados = open(str(filenamein) + str(nr_fog) + '.tmp', 'r')
		tamanho_dados_entre_fogs = open(str(filenameout) + str(nr_fog) + '.tmp', 'a')
		cont = 1
		linetp = []
		for line in FileTemp.readlines():
			line_list = line.split()
			linetp.append(line_list)
		while cont < len(linetp):
			if (linetp[cont][4] == linetp[cont - 1][4]):
				date1 = int(datetime.datetime.strptime(str(linetp[cont][2]) + ' ' +str(linetp[cont][3]), '%Y-%m-%d %H:%M:%S').strftime("%s"))
				date2 = int(datetime.datetime.strptime(str(linetp[cont - 1][2]) + ' ' +str(linetp[cont - 1][3]), '%Y-%m-%d %H:%M:%S').strftime("%s"))
				diffhour = abs(date2 - date1)
				sizemsg = 185 * diffhour
		
				tamanho_dados_entre_fogs.write(str(linetp[cont][4]) + ' ' + str(linetp[cont - 1][4]) + ' ' + str(linetp[cont][5]) + ' ' + str(linetp[cont - 1][5]) + ' ' + str(diffhour) + ' ' + str(sizemsg) +   '\n')


			cont = cont + 1


		tamanho_dados_entre_fogs.close()
		arq_dados_organizados.close()	
			



#FileName = 'qntd_enviado'
FileName = 'connection_made_' #file contains all connection of each fog
FileName2 = 'nr_conexoes_ate_'#file contains all data of the fogs until the number of fog installed
FileName3 = 'dados_organizados_ate_'# storage the data ordered 
FileName4 = 'size_dados_ate_'#files contains the connections with the size of each message and the time between fogs.
RANGE_FOG = 300
FOG_INICIO = 0
FOG_FIM = 6000
FOG_STEP = 500
#FileTemp = open(str(FileName) + '.tmp', 'a')
#FileTemp2 = open(str(FileName2) + '.tmp', 'a')
fog_nodes_list = sql_sbrc2018('Stops')
bus_nodes_list = sql_sbrc2018('FilteredPositions')
#FileTemp = open('fog_connection_5000-5500.tmp', 'a')
#FileTemp2 = open('dados_org_5000-5500.tmp', 'a')
for fog_node in fog_nodes_list:
		 
	qntd_recebidos = 0
	id_fog_node = fog_node[0]
	FileTemp = open('test_files/' + str(FileName) + str(id_fog_node) + '.tmp', 'a')
	coord_fog_node = (fog_node[1], fog_node[2])	
	for bus_node in bus_nodes_list:
		
		bus_coord_node = (bus_node[3], bus_node[4])
		distance = vincenty(bus_coord_node, coord_fog_node).meters #calculate the distancy between fog and bus at momento of connection
		
		if (distance <= RANGE_FOG):#only write in the file if the bus was inside the range of fog. 
			

			FileTemp.write(str(id_fog_node) + " " + str(bus_node[1]) + " " + str(bus_node[2]) + " " + str(bus_coord_node) + "\n")
						
	FileTemp.close()

acc_data_fogs(FOG_INICIO, FOG_FIM, FOG_STEP, FileName, FileName2)
organizando_dados_nr_conexoes(FOG_INICIO, FOG_FIM, FOG_STEP, FileName2, FileName3)
size_msg_entre_fog(FOG_INICIO, FOG_FIM, FOG_STEP, FileName3, FileName4)





