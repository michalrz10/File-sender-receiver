import socket
import os

def receive():
	so=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	so.connect(('8.8.8.8',80))
	hostt=so.getsockname()[0]
	so.close()
	os.chdir('path')		#path where files will be saved
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(0.1)
	iii=0
	host=''
	for i in range(len(hostt)):
		if hostt[i]=='.':
			iii+=1
		host+=hostt[i]
		if iii==3:
			break
	powo=False
	for i in range(1,256):		#trying to connect to all sockets
		try:
			hos=host+str(i)
			s.connect((hos,50000))
			powo=True
			break
		except:
			s.close()
			s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(0.05)
			pass
        
	if powo:			#if connected
		s.settimeout(50)
		print('Connected to '+ hos)
		data=s.recv(1024)
		b=int(str(data,'utf-8'))
		st=[]
		li=[]
		for i in range(b):
			data=s.recv(1024)
			st.append(str(data,'utf-8'))
			data=s.recv(1024)
			li.append(int(str(data,'utf-8')))
		l=0
		for i in li:
			l+=i
		p=[]
		while len(p)<l:
			data=s.recv(1024)
			p+=data
		ile=0
		s.close()
		for i in range(len(st)):
			x=open(st[i],'wb')
			x.write(bytes(p[ile:ile+li[i]+1]))
			ile+=li[i]
			x.close()
		s.close()
		print('Received!')
	else:
		print('Cannot connect!')
