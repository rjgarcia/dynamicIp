#!/usr/bin/env python
# -*- coding: utf-8 -*-



from HTMLParser import HTMLParser
import urllib, smtplib, os
from time import gmtime, strftime
try:
	import ConfigParser
	Config = ConfigParser.ConfigParser()
	configFile = "/etc/dynamicIp/dynamicIp.cfg"
	Config.read(configFile)
except:
	print("Ha habido un problema al cargar el archivo de configuración 	\"/etc/dyamicIp/dyamicIp.conf\", revíselo por favor")

def send_mail_google(sender = "",recipient = "", subject = "", body ="",password = ""):
	#SMTP_SERVER = 'smtp.gmail.com'
	#SMTP_PORT = 587
	
	#smtplib.set_debuglevel(3)
	
	
	
	SMTP_SERVER = Config.get('ConfigServer','SMTP')
	SMTP_PORT = Config.get('ConfigServer','SMPTPort')

	print (SMTP_SERVER + " " + SMTP_PORT)

	body = "" + body + ""
 
	headers = ["From: " + sender,
		   "Subject: " + subject,
		   "To: " + recipient,
		   "MIME-Version: 1.0",
		   "Content-Type: text/html"]
	headers = "\r\n".join(headers)
	
	print (headers)
	
	session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
	session.ehlo()
	session.starttls()
	session.ehlo
	session.login(sender, password)
	
	
	
	session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
	session.quit()

		
		
class MiIPdinamica(HTMLParser):

	def handle_data(self, data):
		if "Address" in data : 
			cad = data.split(":")
			self.ip = cad[1].lstrip()	
			
	def get_ip(self):
		return self.ip   

	
def getExternalIP():
	f = urllib.urlopen("http://checkip.dyndns.org")
	pag_web = f.read()	
	parser = MiIPdinamica()
	parser.feed(pag_web)
	ip = parser.get_ip()
	parser.close()
	f.close()
	return ip


def getlastIP():
	try:
		fileHandle = open ('/var/log/dynamic_ip/dynamic_ip.log',"r" )
	except:
		print("Error al intentar abrir el archivo de log \"/var/log/dynamic_ip/dynamic_ip.log\"")
		exit(1)
		
	lineList = fileHandle.readlines()
	fileHandle.close()
	
	if len(lineList) > 100: 
		try:
			os.system("rm /var/log/dynamic_ip/dynamic_ip.log")
			file = open('/var/log/dynamic_ip/dynamic_ip.log', 'a+')
			file.write(lineList[-1])
			file.close()
		except:
			pass
	if len(lineList) > 0:
		ip = lineList[-1].split("\t")
		ip = ip[1].split("\n")
	else:
		ip = [0]
		
	return ip[0]
			

	
def checkIP():
	print (Config.get('ConfigAccount','Username') + " " + Config.get('ConfigAccount','Username') + " " + "Ip Dinámica servidor" + " " + getExternalIP() + " " + Config.get('ConfigAccount','Password'))
	if getExternalIP() == getlastIP():
		print "\n son iguales"
	else:
		try:
			file = open('/var/log/dynamic_ip/dynamic_ip.log', 'a+')
			file.write(strftime("%d-%m-%Y %H:%M:%S", gmtime()) + "\t" + getExternalIP() + "\n")
			file.close()			
		except:
			print("Error al intentar abrir el archivo de log \"/var/log/dynamic_ip/dynamic_ip.log\"")
			exit(1)
		
		try:
			send_mail_google(Config.get('ConfigAccount','Username'),Config.get('ConfigAccount','Username'),"Ip Dinámica servidor",getExternalIP(),Config.get('ConfigAccount','Password'))	
		except smtplib.SMTPException as e:
			print e
			print("No se ha podido enviar el email a: " + Config.get('ConfigAccount','Username'))
		#send_mail_google("lestatmer@gmail.com","lestatmer@gmail.com","Ip Dinámica servidor",getExternalIP(),"patatapatata")
		
if __name__ == "__main__":

	checkIP()
	
	
	
	
	
	
