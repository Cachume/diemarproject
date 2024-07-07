from tkinter import *
from tkinter import ttk

class arduinopu(Toplevel):
    
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Seleccion un puerto")
        self.geometry("300x100")

        label = Label(self, text="Selecciona tu puerto de arduino para conectarse:")
        label.pack(pady=5)

        self.cpuerto = ttk.Combobox(self, state="readonly", values=['COM2','COM3','COM4','COM5','COM6','COM7','COM8'])
        self.cpuerto.pack(pady=5)

        self.submit_button = Button(self, text="Aceptar", command=self.save_password)
        self.submit_button.pack(pady=10)
        
        self.parent = parent

    def save_password(self):
        self.parent.puerto = self.cpuerto.get()
        self.destroy()