# -*- coding: utf-8 -*-
import threading
import time
import psycopg2
import datetime
import PIL
from PIL import ImageTk
from Tkinter import *
import Tkinter as tk
import threading
import tkFont

id1 = 0
temperatura = 0
uv = 0
humedad = 0
propaganda= ""
recomendacion = "error"
recomendacion2 = "error"
switch_p_r = 0
banderascroller = 0
  
     
def contadorSwitch():
    bandera1 = 1
    global switch_p_r
    global banderascroller
    while(1):
        for m in range(0,1):
            for s in range(0,31):
                time.sleep(1)
                print(s)
        if switch_p_r == 1:
            switch_p_r = 0
        else:
            switch_p_r = 1
        print("variable de cambio = ", switch_p_r)
        banderascroller = 1
            

def extractBD():
    # Extraccion Base de Datos
    global uv
    global temperatura
    global humedad
    global propaganda
    global recomendacion
    global recomendacion2 
    while(1):
	    # Al ser una base de datos privada no es posible dar la clave. 
        try:
            connection = psycopg2.connect(user = "pgmultisistemas",
                                          password = "",
                                          host = "multisistemas.com.co",
                                          port = "5432",
                                          database = "dbmultisistemas")

            cursor = connection.cursor()
            # Print PostgreSQL Connection properties
            print ( connection.get_dsn_parameters(),"\n")


            # Extraer de postgres
            cursor = connection.cursor()
            cursor.execute("SELECT dat_id, tempout, uvindex, outhum, windspeed FROM estaunica WHERE dat_id IN (SELECT MAX(dat_id) FROM estaunica)")
            rows = cursor.fetchall()

	    
            for data in rows:
                id1=str(data[0])
                temperatura= data[1]
                uv= data[2]
                humedad= data[3]
               
                print("id : " + id1)
                print("temperatura : " + data[1])
                print("uv : " + data[2])
                print("humedad : " + data[3])

            cursor.execute("SELECT texto FROM semaforosolar")
            rows = cursor.fetchall()

            for data in rows:
                #print("id : " + str(data[0]))
                propaganda= data[0]
                print("propaganda : " + propaganda)

            if float(uv) <= 2:
                recomendacion = "Disfruta el día, no es"+'\n'+"necesario usar bloqueador"
            if float(uv) > 2 and float(uv) <= 5:
                recomendacion = "Permanece a la sombra al medio día"+'\n'+"usa bloqueador de 6-10 FPS"
            if float(uv) > 5 and float(uv) <= 8:
                recomendacion = "Protégete del sol usando camisa, gafas"+'\n'+"y sombrero, usar bloqueador de 10-25 FPS"
            if float(uv) > 8 and float(uv) <= 10:
                recomendacion = "Evita salir al medio día, usar"+'\n'+"bloqueador de 25-50 FPS"          
            if float(uv) > 10:
                recomendacion = "Utiliza protector de"+'\n'+"50+ FPS obligatoriamente"
            print(recomendacion)
            if float(temperatura) <= 13:
                recomendacion2 = "No olvides tus guantes"+'\n'+"y chamarra, hara frio"
            if float(temperatura) > 13 and float(temperatura) <= 17:
                recomendacion2 = "El clima esta perfecto"+'\n'+"no te compliques"
            if float(temperatura) > 17 and float(temperatura) <= 25:
                recomendacion2 = "Procura usar locion"+'\n'+"y maquillaje suaves"
            if float(temperatura) > 25:
                recomendacion2 = "Procura usar lociones"+'\n'+"suaves y no olvides el desodorante"
            print(recomendacion2)
                
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")
                    time.sleep(5)
                           

def pantalla():
    root = tk.Tk()
    image = PhotoImage(file="background.gif")
    
    background=Label(root, image=image)
    background.place(x=0,y=0,relwidth=1, relheight=1)
 
    temperature = StringVar()
    temperature.set("----"+" °C")		

    Uv = StringVar()
    Uv.set("----"+" %")		
    
    rec1 = StringVar()
    rec1.set("----")

    rec2 = StringVar()
    rec2.set("----")

    temperatureLabel = Label(root, fg="white", background="#00dbde", textvariable=temperature, font=("Helvetica", 40,"bold"))
    temperatureLabel.place(x=580, y=15)

    UvLabel = Label(root, fg="white", background="#00dbde", textvariable=Uv, font=("Helvetica", 40,"bold"))
    UvLabel.place(x=580, y=70)

    rec1Label = Label(root, fg="white", background="#00dbde", textvariable=rec1, font=("Helvetica", 20,"bold"))
    rec1Label.place(x=30, y=150)

    rec2Label = Label(root, fg="white", background="#00dbde", textvariable=rec2, font=("Helvetica", 20,"bold"))
    rec2Label.place(x=500, y=180)

    def exit():
	    root.quit()

    root.attributes("-fullscreen",False)
    
    while(1):
        root.after(6000, exit)   
        root.mainloop()
        temperature.set(temperatura+" °C")
        Uv.set("uv "+uv)
        rec1.set(recomendacion)
        rec2.set(recomendacion2)

# Main

hilo1 = threading.Thread(target=extractBD)
hilo1.start()
time.sleep(3)
hilo2 = threading.Thread(target=pantalla)
hilo2.start()
hilo3 = threading.Thread(target=contadorSwitch)
#hilo3.start()


