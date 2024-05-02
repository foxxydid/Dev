from time import sleep
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import *
import subprocess

#setup mqtt
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("$SYS/#")    
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))    
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("192.168.0.2",1883,60)

#setup tkinter
root = tk.Tk()
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

def update_btn_text():
    if(btn["text"]=="production"):
        btn.configure(text="trial")
        mqttc.publish('HEADER2/state','{"values":[{"id":"trial"},"V":["MC-1"],"q":true]}')
    elif(btn["text"]=="trial"):
        btn.configure(text="maintenance")
        mqttc.publish('HEADER2/state','{"values":[{"id":"maintenance"},"V":["MC-1"],"q":true]}')
    elif(btn["text"]=="maintenance"):
        btn.configure(text="trouble")
        mqttc.publish('HEADER2/state','{"values":[{"id":"trouble"},"V":["MC-1"],"q":true]}')
    elif(btn["text"]=="trouble"):
        btn.configure(text="production")
        mqttc.publish('HEADER2/state','{"values":[{"id":"production"},"V":["MC-1"],"q":true]}')
        
def update_btn_text2():
    if(btn2["text"]=="change"):
        btn2.configure(text="changed")
        valinput = setinput.get()
        mqttc.publish('HEADER1/state',valinput)
        btn2.configure(text="change")
        sleep(3)
        
def update_btn_text3():
    pop = subprocess.Popen("exec " + "onboard",stdout= subprocess.PIPE, shell=True)

label = Label(root, text="change mode", bg='white')
label.pack(pady=10)

btn = tk.Button(root, text="production", command=update_btn_text)
btn.pack()

label2 = Label(root, text="input production")
label2.pack(pady=10)

setinput = tk.Entry(root, bd=5)
setinput.pack()

btn2 = tk.Button(root, text="change", command=update_btn_text2)
btn2.pack()

btn3 = tk.Button(root, text="showkeyboard", command=update_btn_text3)
btn3.pack()

root.mainloop()
