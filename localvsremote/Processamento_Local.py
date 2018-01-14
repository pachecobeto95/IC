#!/usr/bin python -u
#Author: Roberto Goncalves Pacheco
#E-mail: robertopvc@gmail.com
#Institution: UERJ
#Description: This code creates a connection by socket between server and Arduino as client.
#Import these libraries

import socket
import os
import time

FileName = 'CenarioTest1'
Host = ''
Port = 3030
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((Host,Port))
tcp.listen(1)
SampleNumber = 5
PossiveisInter = [5, 10, 20, 25, 30, 35, 40, 45, 50, 100, 150, 200, 250, 300, 350, 400, 500]
connection, client = tcp.accept()
print 'Conectando com ' + str(client)

for i in range(0,SampleNumber):
	time.sleep(1)
	#connection, client = tcp.accept()
	for inter in PossiveisInter:
		FileTemp = open(str(FileName) + "_" + str(inter) + ".tmp", 'a')
		connection.send('s')
		connection.send(str(inter) + "\n")
		connection.send('a')
		InterTime = connection.recv(1024)
		print 'Tempo recebido igual a ', InterTime, inter
		connection.send('f')
		FileTemp.write(str(0) + " " + str(InterTime) + "\n")
		FileTemp.close()
	os.popen("./ic.awk nrvar=1 ic=95 " + str(FileName) + "_" + str(inter) + ".tmp" + " > " + str(FileName) + "_" + str(inter) + ".dt")	
connection.close()
	
	
	
	
	
	
