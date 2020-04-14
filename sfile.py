import socket
import os


def dataLength(length,size):
	tab=[]
	for i in range(size):
		tab.append(int(length/256**(size-1-i)))
		length-=tab[i]*256**(size-1-i)
	return tab
	
def arraytoint(tab):
	number=0
	for i in range(len(tab)):
		number+=tab[i]*256**(len(tab)-1-i)
	return number
	
def gethost():
	so=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	so.connect(('8.8.8.8',80))
	host=so.getsockname()[0]
	so.close()
	return host

def send():
	os.chdir('<path from all files will be sended>')
	filenames=os.listdir()
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.bind(('',50001))
	a,_=sock.recvfrom(4)
	sock.close()
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('.'.join([str(i) for i in list(a)]),50002))
	s.send(bytes(dataLength(len(filenames),2)))
	for filename in filenames:
		file=open(filename,'rb')
		data=file.read()
		if len(data)==0: continue
		s.send(bytes(dataLength(len(bytes(filename,'utf-8')),2)))
		s.send(bytes(filename,'utf-8'))
		s.send(bytes(dataLength(len(data),4)))
		s.send(data)
		file.close()
	s.close()
	
def receive():
	host=gethost()
	os.chdir('<path where to save all files>')
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.sendto(bytes([int(i) for i in host.split('.')]),('<broadcast>',50001))
	sock.close()
	sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host, 50002))
	sock.listen(1)
	s, address = sock.accept()
	for _ in range(arraytoint(list(s.recv(2)))):
		size=arraytoint(list(s.recv(2)))
		data=s.recv(size)
		file=open(str(data,'utf-8'),'wb')
		size=arraytoint(list(s.recv(4)))
		sended=0
		while sended<size:
			data=s.recv(min(1024,size-sended))
			sended+=len(data)
			file.write(data)
		file.close()
	sock.close()
	s.close()
