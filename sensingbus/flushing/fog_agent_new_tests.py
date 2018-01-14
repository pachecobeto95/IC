#Author: Roberto Goncalves Pacheco
#Universidade do Estado do Rio de Janeiro (UERJ)
#Departamento de Eletronica e Telecomunicacoes
#Project: Sensing Bus
#Subject: Comunication between Cloud and Fog


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from signal import signal, SIGPIPE, SIG_DFL
from urlparse import parse_qs
import json
import requests
import time
import datetime
import threading, Queue
import sys
import zlib
from scipy.interpolate import UnivariateSpline
from scipy.signal import lfilter
import matplotlib.pyplot as plt
#import hot_island
#import controller2
#import Module

signal(SIGPIPE, SIG_DFL)

SERVER_CERTS = '/home/pi/ssl/ca-chain.cert.pem' #To verify server
STOP_ID = 1 #This raspberrie's id
MEASUREMENTS_URL = 'https://sensingbus.gta.ufrj.br/measurements_batch_sec/' #Endpoint of insertion api
URL_TEST = '192.168.0.13'
QUEUE_TIME = 86400
QUEUE_TIME2 = 3600
# Variables for server-side validation:
PRIMARY_KEY='/home/pi/ssl/raspberry.key.pem'
LOCAL_CERTIFICATE='/home/pi/ssl/raspberry.cert.pem'
COMPRESSION_LEVEL=1
WORD_SIZE_BITS=-15
MAX_MEASURES=100
MEM_LEVEL=9
STOP_ID = 1
OFFSET=1
FileName = 'gain'
q = Queue.Queue()
deltat=[]
sizeGain=[]
FileName = 'volumedata_nrfog_100.tmp'


def createGraphics ():
    x_axis = range(OFFSET, 20*len(sizeGain)+OFFSET, 20)
    fig, sGPlot = plt.subplots()
    smooth_sizeGain = UnivariateSpline (x_axis, sizeGain)
    sGPlot.plot(x_axis, smooth_sizeGain(x_axis), 'b-')
    #sGPlot.plot(x_axis, sizeGain, 'b-')

    dtPlot = sGPlot.twinx()
    n = 1000  # the larger n is, the smoother curve will be
    b = [1.0 / n] * n
    smooth_deltat = lfilter(b, 1, deltat)
    dtPlot.plot(x_axis, smooth_deltat, 'r-')
    #dtPlot.plot(x_axis, deltat, 'r-')

    sGPlot.set_xlabel('(Numero de Tuplas)')
    sGPlot.set_ylabel('Reducao de Tamanho (%)', color='b')
    dtPlot.set_ylabel('Tempo de Compressao (ms)', color='r')

    fig.tight_layout()
    plt.show()
    plt.close()
    return

def compressMessage (message):
    """Compress Fog Message"""  
    FileName = 'volumedata_nrfog_6_3600.tmp'
    compressOBJ = zlib.compressobj(COMPRESSION_LEVEL, zlib.DEFLATED, WORD_SIZE_BITS, MEM_LEVEL, zlib.Z_HUFFMAN_ONLY)
    #compressOBJ.flush(zlib.Z_SYNC_FLUSH)
    #print message
    messageText = json.dumps(message)
   
    size1 = float(len(messageText))
    messageText = messageText.encode('utf-8').encode('zlib_codec')
 
    t1 = time.time()
    messageText = compressOBJ.compress(messageText)
    messageText += compressOBJ.flush()
    t2 = time.time()

    size2 = float(len(messageText))
    #print size2
    dt = float("{:.2}".format((t2-t1)*1000))
    #print size2
    deltat.append(dt)
    sizeGain.append("{:.0f}".format(size2/size1*100))
    gain = (size2/size1)*100
    #print "num medidas: ", len(deltat)
    FileTemp = open(str(FileName), 'a')
    FileTemp.write(str(size1) + ' ' + str(size2) + ' ' + str(gain) + ' ' + str(t1) + ' ' + str(t2) + '\n')
    if (len(deltat)==MAX_MEASURES):
        #createGraphics ()
        del deltat[:]
        del sizeGain[:]
    #print sizeGain
    #print deltat

    return messageText

def send_thread(thread_name,q):
    """Sends periodically stored data"""
    while True:
        output = {}
        output['stop_id'] = STOP_ID
        output['batches'] = []
        if not q.empty():
            while not q.empty():
                b = q.get()
                if ( b is not None):
                    output['batches'].append(b)
	    message = compressMessage(output)
	    
            #print cloud_client(message)    
            time.sleep(QUEUE_TIME2)

def cloud_client(payload):
    """ Sends mensage to Cloud"""
    #r = requests.post(MEASUREMENTS_URL,
                    #json=payload,
                    #verify=SERVER_CERTS,
                    #cert=(LOCAL_CERTIFICATE, PRIMARY_KEY))
    r = requests.post(URL_TEST, json=payload)
    return r.json
	
    #print r

class S(BaseHTTPRequestHandler):
    def _set_headers(self): 
        """Creates header HTTP requisition"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/x-www-form-urlencoded')
        self.end_headers()

    def do_POST(self): 
        """Receives data from Arduino and sends to Cloud"""
    	input_batches = {}
    	postvars = parse_qs(self.rfile.read(int(self.headers['Content-Length'])),
                                            	keep_blank_values=1)
	#print postvars
    	input_batches['node_id'] = postvars['node_id'][0]
    	for line in postvars['load']:
        	tmp = line.split('\n')
	#print tmp
	#sizetmp = float(len(tmp))
	#print sizetmp
	#print '_______________'
	#hot_island.cartridge(tmp)
	#module = Module.module(tmp)
	#module.controller()
	#cloud_client(module.get_payload())	                
    	input_batches['type'] = str(postvars['type'][0])
    	input_batches['header'] = str(postvars['header'][0])
    	input_batches['received'] = str(datetime.datetime.now())
    	input_batches['load'] = tmp[0:-1] #the last line is always empty 
    	q.put(input_batches)
	#self.send_response(200)
    	return

def run(server_class=HTTPServer, handler_class=S, port=50000):
    """Generates a server to receive POST method"""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting Server Http'
    t = threading.Thread( target = send_thread, args=('alt',q))
    t.daemon = True
    t.start()
    httpd.serve_forever()
    t.join()

if __name__ == "__main__":
    run()
