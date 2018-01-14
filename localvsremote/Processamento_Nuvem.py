#!/usr/bin python -u

#Author: Roberto Goncalves Pacheco
#E-mail: robertopvc@gmail.com
#Institution: UERJ
#Description: This code creates a connection by socket between server and Arduino as client.
#Import these libraries
import socket 
import os     
import sys
import math
import time
from decimal import *



def superpi():
	a = Decimal(1.0)
	b = Decimal(1.0/math.sqrt(2))
	t = Decimal(1.0)/Decimal(4.0)
	p = Decimal(1.0)
		
	for i in range(0, 100):
		at = Decimal((a+b)/2)
		bt = Decimal(math.sqrt(a*b))
		tt = Decimal(t - p*(a-at)**2)
		pt = Decimal(2*p)

		a = at; b = bt; t = tt; p = pt
	
	global my_pi
	my_pi = (a+b)**2/(4*t)
	
	accuracy = 100*(Decimal(math.pi)-my_pi)/my_pi
	#print " Pi is approximately: ", my_pi
	#print " Accuracy is approximately", accuracy
	

	return my_pi, accuracy

Host = ''     #host as localhost or loopback address, 127.0.0.1	
Port = 5000  #port that socket will connect
FileName = 'LatencyTest3'
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp socket
tcp.bind((Host, Port)) #open a connection on this address
tcp.listen(1) #maximum connection that the socket supports
j = 0
timeAcc = 0
SampleNumber = 5
PossiveisInter = [10, 20, 25, 30, 35, 40, 45, 50, 100, 150, 200, 250, 300, 350, 400, 500]
LatenciaInduzida = [0, 10, 50, 100, 200, 300, 400, 500]
connection, client = tcp.accept() #accept socket connection, because it's tcp
print 'Conectando com: ', client
for latenciainduzida in LatenciaInduzida:
	print "A latencia induzida: ", latenciainduzida
	time.sleep(3)
	os.popen("tc qdisc add dev eth0 root netem delay " + str(latenciainduzida) + "ms")
	#FileTemp = open(str(FileName) + "_" + str(latenciainduzida) + ".tmp", 'w')
	for i in range(0, SampleNumber): 
		time.sleep(1)
		print " A amostra e: ", i
		for inter in PossiveisInter:
			FileTemp = open(str(FileName) + "_" + str(inter) + ".tmp", 'a')
			timeAcc = 0
			j = 0
			#ini = time.time()	
			print "A interatividade e: ", inter	
			while j < inter: 
				connection.send('s')
				dados = connection.recv(1024)
				print 'Recebido a string', dados
				superpi()
				connection.send('p')
				connection.send(str(my_pi) + "\n")
				#time.sleep(1)
				#connection.send('w')
				connection.send('t')
				timez = connection.recv(1024)
				timeAcc += int(timez)
				print 'Recebido timez ' + str(timez) + " " + str(timeAcc)
				connection.send('f')
				j = j + 1
				print ' j e igual: ', j	
			#fim = time.time()
			#SuperPiTime = fim - ini	
			#print 'Tempo por de processamento python', SuperPiTime
			#FileTemp.write(str(inter) + "  " + str(timeAcc) + "\n")
			FileTemp.write(str(latenciainduzida) + "  " + str(timeAcc) + "\n")
		#os.popen("./ic.awk nrvar=1 ic=95 " + str(FileName) + "_" + str(inter) + ".tmp" + " > " + str(FileName) + "_" + str(inter) + ".dt")

	os.popen("tc qdisc del dev eth0 root netem")
	FileTemp.close()
	#os.popen("./ic.awk nrvar=1 ic=95 " + str(FileName) + "_" + str(inter) + ".tmp" + " > " + str(FileName) + "_" + str(inter) + ".dt")
connection.close()





