from tkinter import *
from tkinter import ttk, Menu, messagebox
from PIL import Image, ImageTk

class Leds(Tk):
    estadoboton = True
    estadoarduino = True
    def __init__(self):
        super().__init__()
        self.title("Sistema | Leds")
        self.geometry("400x400")
        self.resizable(0,0)
        self.config(bg="#ffffff")
        # self.imagenframe = PhotoImage(file="./assets/0000.png")
        # self.imagen_led = Label(self, image=self.imagenframe,background="#283f9b")
        # self.imagen_led.pack(pady=10)
        Label(self, text="Previsualizacion de leds",font=('Arial',14,"bold"),background="#283f9b",fg="#ffffff")
        Label(self, text="Configuracion de los leds",
              font=("Arial",14,"bold"),bg="#ffffff",fg="#283f9b").pack(pady=10)
        
        #Variable de los leds
        self.led1_var = IntVar()
        self.led2_var = IntVar()
        self.led3_var = IntVar()
        self.led4_var = IntVar()
        #Leds de la interfaz
        self.led1 = Checkbutton(self, text="1", font=("Arial",11,"bold"),bg="#ffffff" ,variable=self.led1_var)
        self.led2 = Checkbutton(self, text="2", font=("Arial",11,"bold"),bg="#ffffff" ,variable=self.led2_var)
        self.led3 = Checkbutton(self, text="3", font=("Arial",11,"bold"),bg="#ffffff" ,variable=self.led3_var)
        self.led4 = Checkbutton(self, text="4", font=("Arial",11,"bold"),bg="#ffffff" ,variable=self.led4_var)
        #Mostrar los leds
        self.led1.place(y=120, x=80)
        self.led2.place(y=120, x=150)
        self.led3.place(y=120, x=220)
        self.led4.place(y=120, x=290)
        Label(self,text="Selecciona la funcion para los leds:",
              font=("Arial",11,"bold"),bg="#ffffff", fg="#283f9b").pack(pady=40)
        self.combox = StringVar()
        #Combobox Interfaz
        self.comboopciones = ttk.Combobox(self,state="readonly",textvariable=self.combox,
                     values=['Encender', 'Parpadeo','Encender desde izquierda','Encender desde derecha','Apagar'])
        self.comboopciones.place(y=190, x=90, width=220, height=25)
        #Boton de inicio
        self.botonaccion = Button(self,
                                  text="Empezar",
                                  fg="#ffffff",
                                  bg="#2ed32a",
                                  font=("Arial",12,'bold'),
                                  border=0,
                                  command=self.Ledstart)
        self.botonaccion.place(x=155, y=250)
    def Ledstart(self):
        confirmacion = False
        modo = self.combox.get()
        leds = str(self.led1_var.get())+str(self.led2_var.get())+str(self.led3_var.get())+str(self.led4_var.get())
        if self.estadoboton:
            if modo == "":
                messagebox.showerror(title="Error", message="No has seleccionado un modo para los leds")
            elif modo == "Encender":
                print(modo)
                print(leds)
                self.imagenmostrar= PhotoImage(file="assets/"+leds+".png")
                self.imagen_led.config(image=self.imagenmostrar)
                confirmacion = True
            elif modo == "Parpadeo":
                print(modo)
                gif_path = "assets/leds/Parpadeo/"+ leds + ".gif"
                print(gif_path)
                self.frames_num = 2
                self.gif_path = gif_path
                self.frames = [PhotoImage(file=self.gif_path, format=f"gif -index {i}") for i in range(self.frames_num)]
                self.current_frame = 0
                self.animacionled = True
                self.update_frame()
                confirmacion = True

            if confirmacion == True:
                self.botonaccion.config(text="Detener",
                                fg="#ffffff",
                                bg="#d32a2a",)
                for led in [self.led1,self.led2,self.led3,self.led4,self.comboopciones]:
                    led.config(state="disable")
                self.estadoboton = False
        else:
            self.botonaccion.config(text="Comenzar",
                                    fg="#ffffff",
                                    bg="#2ed32a",)
            for led in [self.led1,self.led2,self.led3,self.led4,self.comboopciones]:
                led.config(state="normal")
            self.imagenmostrar= PhotoImage(file="assets/0000.png")
            self.imagen_led.config(image=self.imagenmostrar)
            self.animacionled = False
            self.estadoboton = True 

    def update_frame(self):
        """Actualiza la imagen del gif"""
        if self.animacionled:
            frame = self.frames[self.current_frame]
            self.current_frame = (self.current_frame + 1) % self.frames_num
            self.imagen_led.configure(image=frame)
            self.imagen_led.after(1000, self.update_frame) 
if __name__ == "__main__":
    app = Leds()
    app.mainloop()