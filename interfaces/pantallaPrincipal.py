from tkinter import *
from tkinter import Menu, messagebox
import serial
import time
#from models.systemdb import Pydb

class MainScreen(Tk):

    automatico = False
    tiemp = 0
    def __init__(self, user_info):
        super().__init__()
        self.user_session = user_info
        self.title("Sistema Proyecto")
        self.geometry("850x500")
        self.config(bg="#b4aca4")
        self.resizable(0,0)
        self.imagen = PhotoImage(file="assets/casa2.png")
        self.imagent = PhotoImage(file="assets/temperatura.png")
        self.imagenh = PhotoImage(file="assets/humedad.png")
        
        self.casaf = Frame(self,bg="#b4aca4")
        self.casaf.place(x=0,y=0)
        self.casad = Frame(self,bg="#b4aca4",width=200,height=430)
        self.casad.place(x=650,y=0)
        #self.db=Pydb()
        self.arduino()
        self.create_labels()
        #self.actualizar_interfaz()
    
    def create_labels(self):
        Label(self.casaf,bg="#b4aca4" ,fg="#ffffff",text="¡Bienvenido de Nuevo!",font=("Helvetica", 20, 'bold')).pack(pady=10)
        Label(self.casaf,bg="#b4aca4" ,image=self.imagen).pack()
        self.Cuarto2 = Button(self.casaf, text="Encender Cuarto2",fg="#229954", command=lambda: self.luces("Cuarto2"))
        self.Cuarto2.place(x=60, y=400)
        self.Cuarto1 = Button(self.casaf, text="Encender Cuarto1",fg="#229954", command=lambda: self.luces("Cuarto1"))
        self.Cuarto1.place(x=170, y=400)
        self.Cuarto3 = Button(self.casaf, text="Encender Cuarto3",fg="#229954", command=lambda: self.luces("Cuarto3"))
        self.Cuarto3.place(x=70, y=200)
        self.Cuarto4 = Button(self.casaf, text="Encender Cuarto4",fg="#229954", command=lambda: self.luces("Cuarto4"))
        self.Cuarto4.place(x=220, y=200)
    
        # Garage = Button(self.casaf, text="Encender")
        # Garage.place(x=490, y=300)

        self.temperatura = Label(self.casad, image=self.imagent,bg="#b4aca4").place(x=65,y=100)
        self.temperaturai = Label(self.casad,text="Temperatura: 30°",bg="#b4aca4",font=("Helvetica", 12, 'bold'))
        self.temperaturai.place(x=40,y=170)
        self.humedad = Label(self.casad, image=self.imagenh,bg="#b4aca4").place(x=75,y=220)
        self.humedadi = Label(self.casad,text="Humedad: 30%",bg="#b4aca4",font=("Helvetica", 12, 'bold'))
        self.humedadi.place(x=40,y=290)

        self.modos = Button(self.casad, text="Activar Modo Automatico",fg="#229954", command=self.modosluces)
        self.modos.place(x=30,y=390)

    def modosluces(self):
        if not self.automatico:
            comando= "ModoAutomatico"
            self.arduinoc.write(comando.encode())
            self.modos.config(text="Desactivar Modo Automatico",fg="#c0392b")
            self.Cuarto1.config(state="disable")
            self.Cuarto2.config(state="disable")
            self.Cuarto3.config(state="disable")
            self.Cuarto4.config(state="disable")
            self.automatico = True
        else:
            comando= "Salir"
            self.arduinoc.write(comando.encode())
            self.modos.config(text="Activar Modo Automatico",fg="#229954")
            self.Cuarto1.config(state="normal")
            self.Cuarto2.config(state="normal")
            self.Cuarto3.config(state="normal")
            self.Cuarto4.config(state="normal")
            self.automatico = False


    
    def actualizar_interfaz(self):
        self.tiemp= self.tiemp+1
        self.temperaturai.config(text=f"Temperatura: {str(self.tiemp)}°")
        self.after(1000, self.actualizar_interfaz)
    
    def arduino(self):
        try:
            self.arduinoc = serial.Serial("COM5",9600,timeout=1)
            print("Se conecto")
        except:
            print("Error con arduino")
    
    def luces(self,comando):
        if(comando=="Cuarto1"):
            botonc= self.Cuarto1
        elif(comando=="Cuarto2"):
            botonc= self.Cuarto2
        elif(comando=="Cuarto3"):
            botonc= self.Cuarto3
        elif(comando=="Cuarto4"):
            botonc= self.Cuarto4
        print(comando)
        self.arduinoc.write(comando.encode())
        time.sleep(3)
        entrada = self.arduinoc.readline().decode("utf-8").strip()
        if(entrada =="Encendiendo "+comando):
            botonc.config(text="Apagar "+comando,fg="#c0392b")
            print("Se encendio")
        elif(entrada =="Apagando "+comando):
            botonc.config(text="Encender "+comando,fg="#229954")
            print("Se apago")
    
    def exit_program(self):
        self.destroy()
    
    def admin_motor(self):
        print("adminmotor")

if __name__ == "__main__":
    app = MainScreen([1, 'albertq703@gmail.com', '2024-06-29 12:22:46',2])
    app.mainloop()
