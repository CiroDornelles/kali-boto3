#!/usr/bin/env python3
import pystray
import PIL.Image
import threading as th
import time 
import boto3
import subprocess


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
        maquinaKali = ec2instance.Instance("i-02aff84ed2b75de02")
        estado = maquinaKali.state.copy()
        estado = estado["Name"]
        icon.icon = iconeinstancia(estado)
        if button == True and estadoDesejado == estado:
            return
        time.sleep(sleepTime)
        
timer = th.Timer(0.1, estadoInstancia,[300,False,"none"])

def ligar(icon, item):
    ec2instance.Instance("i-02aff84ed2b75de02").start()
    estadoInstancia(10,True,"running")
    
def desligar(icon, item):
    ec2instance.Instance("i-02aff84ed2b75de02").stop()
    estadoInstancia(10,True,"stopped")
    
icon = pystray.Icon("Kali Linux", image, menu=pystray.Menu(
    pystray.MenuItem("ligar instancia", ligar), 
    pystray.MenuItem("Desligar instancia", desligar) 
))



timer.start()
icon.run()