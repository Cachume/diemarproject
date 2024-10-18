from tkinter import *
from tkinter import Menu, messagebox
#from models.systemdb import Pydb

class MainScreen(Tk):


    def __init__(self, user_info):
        super().__init__()
        self.user_session = user_info
        self.title("Sistema Proyecto")
        self.geometry("850x500")
        self.config(bg="#b4aca4")
        self.imagen = PhotoImage(file="assets/casa2.png")
        self.imagent = PhotoImage(file="assets/temperatura.png")
        self.imagenh = PhotoImage(file="assets/humedad.png")
        
        self.casaf = Frame(self,bg="#b4aca4")
        self.casaf.place(x=0,y=0)
        self.casad = Frame(self,bg="#b4aca4",width=200,height=430)
        self.casad.place(x=650,y=0)
        #self.db=Pydb()
        self.create_labels()
    
    def create_labels(self):
        Label(self.casaf,bg="#b4aca4" ,fg="#ffffff",text="¡Bienvenido de Nuevo!",font=("Helvetica", 20, 'bold')).pack(pady=10)
        Label(self.casaf,bg="#b4aca4" ,image=self.imagen).pack()
        self.temperatura = Label(self.casad, image=self.imagent,bg="#b4aca4").place(x=65,y=100)
        self.temperaturai = Label(self.casad,text="Temperatura: 30°",bg="#b4aca4",font=("Helvetica", 12, 'bold'))
        self.temperaturai.place(x=40,y=170)
        self.humedad = Label(self.casad, image=self.imagenh,bg="#b4aca4").place(x=75,y=220)
        self.humedadi = Label(self.casad,text="Humedad: 30%",bg="#b4aca4",font=("Helvetica", 12, 'bold'))
        self.humedadi.place(x=40,y=290)

    
    def open_leds(self):
        print("hola")
    
    def open_motor(self):
        print("hola")
    
    def logout(self):
        self.destroy()
    
    def exit_program(self):
        self.destroy()
    
    def admin_motor(self):
        print("adminmotor")

if __name__ == "__main__":
    app = MainScreen([1, 'albertq703@gmail.com', '2024-06-29 12:22:46',2])
    app.mainloop()
