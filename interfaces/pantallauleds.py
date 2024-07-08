from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from models.systemdb import Pydb
from interfaces.arduinopu import arduinopu
import serial as serial
import time

class LedsU(Toplevel):

    puerto = ""
    conexion = False
    def __init__(self):
        super().__init__()
        self.db = Pydb()
        self.animacionled = False  # Inicializar animacionled
        self.frames = []  # Inicializar frames
        self.current_frame = 0  # Inicializar current_frame
        self.frames_num = 0  # Inicializar frames_num
        self.configVentana()
        self.configInterfaz()

    def configVentana(self):
        self.title("Sistema | Leds")
        self.geometry("400x400")
        self.resizable(0, 0)
        self.config(bg="#ffffff")

    def configInterfaz(self):
        self.imagenframe = PhotoImage(file="assets/0000.png")
        self.imagen_led = Label(self, image=self.imagenframe, bg="#000000")
        self.imagen_led.place(x=70, y=320)

        Label(self, text="Manejo de Leds", font=("Arial",18,"bold"),bg="#ffffff").place(y=20,x=110)

        # Combobox Interfaz
        self.comboopciones = ttk.Combobox(self, state="readonly", values=self.obtener_secuencias_disponibles())
        self.comboopciones.place(y=140, x=90, width=220, height=25)

        # Botón para cargar la secuencia seleccionada
        self.boton_cargar = Button(self, text="Cargar Secuencia", command=self.cargar_secuencia)
        self.boton_cargar.place(y=180, x=90, width=220, height=25)

        self.boton_arduino= Button(self, text="Conectar Arduino", command=self.conectar_arduino)
        self.boton_arduino.place(y=210, x=90, width=220, height=25)
        
        self.boton_arduinop= Button(self, text="Cambiar Puerto", command=self.vef_puerto)
        

    def conectar_arduino(self):
        if self.puerto != "":
            if self.conexion == True:
                self.boton_arduino.config(text="Conectar Arduino")
                self.boton_arduinop.config(state="normal")
                self.conexion = False
                print("desconectado")
            else:
                self.conexion = True
                self.boton_arduino.config(text="Desconectar Arduino")
                self.boton_arduinop.config(state="disable")
                print("conectado")
        else:
            self.vef_puerto()
            self.boton_arduinop.place(y=240, x=90, width=220, height=25)

    def vef_puerto(self):
        arduino = arduinopu(self)
        arduino.grab_set()
        arduino.wait_window()
        try:
            conex=serial.Serial(self.puerto,"9600",timeout=2)
            conex.close()
            messagebox.showinfo("Exito al conectar","Arduino conectado con exito")
        except:
            messagebox.showerror("Error al conectar arduino","Error al conectar arduino intenta con otro puerto")

    def obtener_secuencias_disponibles(self):
        secuencias = self.db.obtener_secuencias()
        opciones = [f"{modo} - {leds}" for modo, leds in secuencias]
        return opciones

    def cargar_secuencia(self):
        if self.animacionled:
            self.boton_cargar.config(text="Cargar Secuencia")
            self.boton_arduino.config(state='normal')
            self.detener_animacion()
            if self.conexion == True:
                self.conex=serial.Serial(self.puerto,"9600")
                time.sleep(2)
                comand="apagado"
                self.conex.write(comand.encode())
                self.conex.close()
        else:
            seleccion = self.comboopciones.get()
            if seleccion:
                modo, leds = seleccion.split(' - ')
                if modo == "Parpadeo":
                    self.cargar_gif(leds, 2)
                    if self.conexion == True:
                        self.conex=serial.Serial(self.puerto,"9600")
                        time.sleep(2)
                        comand="p"+leds
                        self.conex.write(comand.encode())
                        self.conex.close()
                elif modo == "Encender desde izquierda":
                    self.cargar_gif(leds, 5, "iz")
                elif modo == "Encender desde derecha":
                    self.cargar_gif(leds, 5, "de")
                else:
                    if self.conexion == True:
                        self.conex=serial.Serial(self.puerto,"9600")
                        time.sleep(2)
                        comand="et"+leds
                        self.conex.write(comand.encode())
                        self.conex.close()
                    self.cargar_imagen_estatica(leds)
                    self.animacionled = True
                    print("et"+leds)
                
            self.boton_cargar.config(text="Detener Secuencia")
            self.boton_arduino.config(state='disable')

    def cargar_imagen_estatica(self, leds):
        self.animacionled = False
        leds_imagen = ''.join(leds.split())
        imagen_path = f"assets/{leds_imagen}.png"
        self.imagenframe = PhotoImage(file=imagen_path)
        self.imagen_led.config(image=self.imagenframe)
        # self.boton_cargar.config(text="Cargar Secuencia")

    def cargar_gif(self, leds, frames_num, suffix=""):
        self.animacionled = True
        leds_gif = ''.join(leds.split())
        gif_path = f"assets/{leds_gif}{suffix}.gif"
        self.frames_num = frames_num
        self.frames = [PhotoImage(file=gif_path, format=f"gif -index {i}") for i in range(self.frames_num)]
        self.current_frame = 0
        self.boton_cargar.config(text="Detener Animación")
        self.update_frame()

    def update_frame(self):
        """Actualiza la imagen del gif"""
        if self.animacionled:
            frame = self.frames[self.current_frame]
            self.current_frame = (self.current_frame + 1) % self.frames_num
            self.imagen_led.configure(image=frame)
            self.imagen_led.after(1000, self.update_frame)

    def detener_animacion(self):
        """Detiene la animación del GIF"""
        self.animacionled = False
        self.imagenframe = PhotoImage(file="assets/0000.png")
        self.imagen_led.config(image=self.imagenframe)
        self.boton_cargar.config(text="Cargar Secuencia")