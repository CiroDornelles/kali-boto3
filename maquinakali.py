#!/usr/bin/python
import pystray
import PIL.Image
import threading as th
import time 
import boto3
from subprocess import Popen
import os 


idInstancia = "i-02aff84ed2b75de02"
pathImagens = "/home/ciro/Documentos/pythonkali/"
ec2instance = boto3.resource("ec2")
images = ["imagens/verde.png","imagens/amarelo.png","imagens/vermelho.png"]
image =  PIL.Image.open(pathImagens + images[2])
##setando icone da instancia 
def iconeinstancia(estado):
    if estado == "stopped":
        image =  PIL.Image.open(pathImagens + images[2])
    elif estado == "running":
        image =  PIL.Image.open(pathImagens + images[0])
    elif estado != "stopped" or estado != "running": 
        image =  PIL.Image.open(pathImagens + images[1])
    return image

def estadoInstancia(sleepTime,button,estadoDesejado):
    var = True
    while var:
        maquinaKali = ec2instance.Instance(idInstancia)
        estado = maquinaKali.state.copy()
        estado = estado["Name"]
        icon.icon = iconeinstancia(estado)
        if button == True and estadoDesejado == estado:
            return
        time.sleep(sleepTime)
        
timer = th.Timer(0.1, estadoInstancia,[300,False,"none"])

def ligar(icon, item):
    ec2instance.Instance(idInstancia).start()
    estadoInstancia(10,True,"running")
    
def desligar(icon, item):
    ec2instance.Instance(idInstancia).stop()
    estadoInstancia(10,True,"stopped")

def sshConnection():
    comando =["konsole" ,"-e" , "ssh" ,"-i" ,"/home/ciro/.ssh/security-team.pem" , "kali@ec2-34-200-170-222.compute-1.amazonaws.com" ]    
    Popen(comando)

def portFowarding():
    pass

def montarDrive():
    pass

def sair():
    pid = os.getpid()
    command = ['kill','-9', str(pid)]
    Popen(command)
    
    
icon = pystray.Icon("Kali Linux", image, menu=pystray.Menu(
    pystray.MenuItem("ligar instancia", ligar), 
    pystray.MenuItem("Desligar instancia", desligar), 
    pystray.MenuItem("Tarefas Administrativas",pystray.Menu(
        pystray.MenuItem("Conexão ssh",sshConnection),
        pystray.MenuItem("Port Fowarding", portFowarding),
        pystray.MenuItem("Montar Drive", montarDrive)
    )),
    pystray.MenuItem("Sair",sair)
))



timer.start()
icon.run()