##intervalo de toma de datos
## salto de linea cuando se guardan los  datos
import serial
import serial.tools.list_ports 
import time
import sys
import os
debug = True

def get_ports():
	a = serial.tools.list_ports.comports() 
	return a

def mide_temperatura(port):
	##letra= input()
	##port.write(letra.encode()) para pasar variable a arduino
	port.write(b'1')																						##comunicacion arduino
	time.sleep(0.005)
	temperatura= (port.readline().decode('ascii'))
	return temperatura

def findArduino(portsFound):
	commPort= []
	longlist= len(portsFound)
	if debug: print(longlist, "Puertos encontrados: ")
	for i in range(longlist):
		port= portsFound[i]
		strPort= str(port)
		if debug: print(strPort)
		if('CH340' in strPort) or ('Arduino Uno' in strPort) or ('USB2.0-Serial' in strPort) or ('USB Serial' in strPort):
			splitPort= strPort.split(' - ')
			commPort.append(splitPort[0])
			print("\n puerto USB que tiene firma arduino: \n")
	print(commPort, "\n")
	return commPort

def getSN(port):
	neoQ_VersionNum=1
	if neoQ_VersionNum == 0:
		sn= str(random.randint(1,10000))
	else:
		port.write(b'2')																				##comunicacion arduino
		sn= port.readline().decode('ascii')
		sn= "SN" + sn.rstrip("\n")
	if debug: print("Serial Number:", sn)
	return sn

def archivo_temperaturas(fecha,hora,data):
	filename= sys.argv[1]
	with open (filename, "ta") as f:
		f.write(fecha)
		f.write(hora)
		f.write(data)
		funcionando(fecha,hora,data)
		f.close() ####TANTEAR ESTE CIERRO CADA VEZ

def archivo_medianas(data):
	filename= "medianas.csv"
	with open(filename, "ta") as f:
		f.write(data )
		f.close()

def fecha():
	fecha=time.strftime('%d/%m/%y') + ","
	return fecha

def hora():
	hora=time.strftime('%H:%M:%S') + ","
	return hora

def espera():
	espera= time.sleep(0.005)
	return espera

def funcionando(fecha, hora, temperatura):
	print(fecha,hora,temperatura)

def intervalo(hora):
	segundos= float(hora) * 60.00 * 60.00
	return segundos

def mediana(temperaturas,mediciones):
	data= sorted(temperaturas)
	index = mediciones // 2

	if mediciones % 2 != 0:
		return data[index]
	return (int(data[index - 1]) + int(data[index])) / 2

def salir():
	exit = os._exit(1)
	return exit

def abrir_puertos(arduinos):
	ard=0
	if len(arduinos)==0:
		FaltaNeoQ= True
		print("No encuentro puerto USB con neoQ")
		sys.exit()
	else:
		connected = False
		p=0
		while( not connected) and (p <= len(arduinos)):
			try:
				ard= serial.Serial(arduinos[p],57600,timeout=2)
				neoQ_SerialNum= getSN(ard)
				connected= True

			except:
				p= p+1
		if not connected:
			print("Error no puedo abrir el puerto USB")
	return ard

def cerrar_puertos(arduinos):
	close=0
	off= False
	i=0
	while(not off) and (p<= len(arduinos)):
		try:
			close= arduinos[p].close()
			off= True
		except:
			p=p+1
	if not off:
		print("ERORR NO PUDE CERRAR LOS PUERTOS\n")
	return close

def cerrar_puertos(arduinos):
	close=0
	off= False
	i=0
	while(not off) and (p<= len(arduinos)):
		try:
			close= arduinos[p].close()
			off= True
		except:
			p=p+1
	if not off:
		print("ERORR NO PUDE CERRAR LOS PUERTOS\n")
	return close


def cerrar_puerto(port):
	port = port.close()
	return port 

def handshaking(port):
	firma= port.write(b'3') 																			##comunicacion arduino
	f= (port.readline().decode('ascii'))
	print("HANDSHAKING:\n",f)
	return f

def principal(port,horas):
	mediciones = 0
	temp_mediana= []
	##archivo_medianas(fecha() + hora())			medianas por ahora no 
	print("mediciones:")
	handshaking(port)
	while mediciones < intervalo(horas):
		temperatura= mide_temperatura(port)
		temp_mediana.append(temperatura)
		archivo_temperaturas(fecha(),hora(),temperatura)
		mediciones= mediciones + 1
		espera()

	archivo_medianas(fecha() + hora() + str(mediana(temp_mediana,mediciones)) + "\n")
	temp_mediana.clear()
	cerrar_puerto(port)
	salir()

	return  temperatura

if __name__ ==  "__main__":				
	puertos= get_ports()				##leo puertos
	arduinos= findArduino(puertos)		## genero lista con puertos arduinos
	print("o")
	puerto_abierto= abrir_puertos(arduinos)	
	print("F")
	principal(puerto_abierto,sys.argv[2])	##le paso el puerto, ojo que aca la lista tiene un elemento para cuando haya más arduinos conectados
											## le paso el argumento n2 q corresponde a las horas de actividad
											## primer argumento que le paso nombre de archivo para las temperaturas