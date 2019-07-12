import socket
import os
from time import sleep


def send():
	os.chdir('path')	#path from which all files will be sent
	b=os.listdir()
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('0.0.0.0',50000))
	s.listen(1)
	(c,a)=s.accept()
	print(a)
	c.send(bytes(str(len(b)),'utf-8'))
	sleep(0.1)
	for i in b:
		try:
			x=open(i,'rb')
		except:
			print('Nie udalo sie wyslac: '+i)
			continue
		data=x.read()
		if len(data)==0: continue
		c.send(bytes(i,'utf-8'))
		sleep(0.1)
		c.send(bytes(str(len(data)),'utf-8'))
		sleep(0.1)
		x.close()
	for i in b:
		try:
			x=open(i,'rb')
		except:
			print('Nie udalo sie wyslac: '+i)
			continue
		data=x.read()
		if len(data)==0: continue
		c.send(data)
		x.close()
	c.close()
	print('Zakonczono!')
