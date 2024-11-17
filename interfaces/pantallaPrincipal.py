from tkinter import *
from tkinter import Menu, messagebox
import serial
import time

class MainScreen(Tk):

    automatico = False
    tiemp = 0
    informacion = False

    def __init__(self, user_info):
        super().__init__()
        self.user_session = user_info
        self.title("Sistema Proyecto")
        self.geometry("850x500")
        self.config(bg="#b4aca4")
        self.resizable(0, 0)
        self.imagen = PhotoImage(file="assets/casa2.png")
        self.imagent = PhotoImage(file="assets/temperatura.png")
        self.imagenh = PhotoImage(file="assets/humedad.png")
        self.imagealert = PhotoImage(file="assets/prevenir.png")

        self.casaf = Frame(self, bg="#b4aca4")
        self.casaf.place(x=0, y=0)
        self.casad = Frame(self, bg="#b4aca4", width=200, height=500)
        self.casad.place(x=650, y=0)

        self.arduino()
        self.create_labels()
        self.actualizar_interfaz()

    def create_labels(self):
        Label(self, bg="#b4aca4", fg="#ffffff", text="¡Bienvenido de Nuevo!", font=("Helvetica", 20, 'bold')).pack(pady=8)
        Label(self.casaf, bg="#b4aca4", image=self.imagen).pack(pady=50)
        self.Cuarto2 = Button(self.casaf, text="Encender", fg="#ffffff",bg="#229954" ,command=lambda: self.luces("Cuarto2"),font=("Helvetica", 10, 'bold'))
        self.Cuarto2.place(x=60, y=400)
        self.Cuarto1 = Button(self.casaf, text="Encender", fg="#ffffff",bg="#229954", command=lambda: self.luces("Cuarto1"),font=("Helvetica", 10, 'bold'))
        self.Cuarto1.place(x=170, y=400)
        self.Cuarto3 = Button(self.casaf, text="Encender", fg="#ffffff",bg="#229954", command=lambda: self.luces("Cuarto3"),font=("Helvetica", 10, 'bold'))
        self.Cuarto3.place(x=70, y=200)
        self.Cuarto4 = Button(self.casaf, text="Encender", fg="#ffffff",bg="#229954", command=lambda: self.luces("Cuarto4"),font=("Helvetica", 10, 'bold'))
        self.Cuarto4.place(x=220, y=200)
        self.Patio = Button(self.casaf, text="Encender", fg="#ffffff",bg="#229954", command=lambda: self.luces("Patio"),font=("Helvetica", 10, 'bold'))
        self.Patio.place(x=350, y=80)
        self.Entrada= Button(self.casaf, text="Encender", fg="#ffffff",bg="#229954", command=lambda: self.luces("Entrada"),font=("Helvetica", 10, 'bold'))
        self.Entrada.place(x=350, y=400)
        self.Sala= Button(self.casaf, text="Encender", fg="#ffffff",bg="#229954", command=lambda: self.luces("Sala"),font=("Helvetica", 10, 'bold'))
        self.Sala.place(x=350, y=200)

        self.temperatura = Label(self.casad, image=self.imagent, bg="#b4aca4").place(x=60, y=50)
        self.temperaturai = Label(self.casad, text="Temperatura: 30°", bg="#b4aca4", font=("Helvetica", 12, 'bold'))
        self.temperaturai.place(x=25, y=120)
        self.humedad = Label(self.casad, image=self.imagenh, bg="#b4aca4").place(x=75, y=160)
        self.humedadi = Label(self.casad, text="Humedad: 30%", bg="#b4aca4", font=("Helvetica", 12, 'bold'))
        self.humedadi.place(x=35, y=225)

        self.autolabel = Label(self.casad, text="Modo Automatico:", bg="#b4aca4", font=("Helvetica", 12, 'bold'))
        self.autolabel.place(x=35, y=400)
        self.modos = Button(self.casad, text="Activar", fg="#ffffff",bg="#229954" ,command=self.modosluces,font=("Helvetica", 10, 'bold'))
        self.modos.place(x=70, y=425)
        self.alertai = Label(self.casad, bg="#b4aca4")
        self.alertai.place(x=70,y=320)

    def modosluces(self):
        if not self.automatico:
            comando = "ModoAutomatico"
            self.arduinoc.write(comando.encode())
            self.modos.config(text="Desactivar",fg="#ffffff",bg="#c0392b")
            self.automatico = True
        else:
            comando = "ModoAutomatico"
            self.arduinoc.write(comando.encode())
            self.modos.config(text="Activar", fg="#ffffff",bg="#229954")
            self.automatico = False

    def actualizar_interfaz(self):
        # Leer información del Arduino
        entrada = self.arduinoc.readline().decode("utf-8").strip()
        if entrada:
            datos = entrada.split("/")
            print(datos)
            self.temperaturai.config(text=f"Temperatura: {str(datos[0])}°")
            self.humedadi.config(text=f"Humedad: {str(datos[1])}%")
            
            # Actualizar estado de los botones
            estados_led = datos[2]
            self.actualizar_botones(estados_led)

            #Verificacion del sensor de humo
            valor_sensor = int(datos[4])
            if valor_sensor >= 200 and not self.informacion:
                self.mostrar_alerta("Se ha detectado la presencia de\n Humo/Gas en la casa")
                self.informacion= True
                self.infogh = Label(self.casad, text="Se ha detectado\n Humo/Gas",fg="#ff3e14" ,bg="#b4aca4", font=("Helvetica", 11, 'bold'))
                self.infogh.place(x=40, y=280)
            elif valor_sensor < 200 and self.informacion:
                self.informacion= False
                self.alertai.config(image="")
                self.infogh.place_forget()
               
            if self.informacion:
                self.imagenpar()


        self.after(500, self.actualizar_interfaz)
    
    def imagenpar(self):
        if self.tiemp == 0:
            self.alertai.config(image=self.imagealert)
            self.tiemp =1
        elif self.tiemp == 1:
            self.alertai.config(image="")
            self.tiemp =0

    def actualizar_botones(self, estados_led):
        botones = [self.Cuarto1, self.Cuarto2, self.Cuarto3, self.Cuarto4,self.Patio,self.Entrada,self.Sala]
        for i, estado in enumerate(estados_led):
            print(f"Índice: {i}, Estado: {estado}")
            if estado == '1':
                botones[i].config(text=f"Apagar", fg="#ffffff",bg="#c0392b")
            else:
                botones[i].config(text=f"Encender", fg="#ffffff",bg="#229954")

    def arduino(self):
        try:
            self.arduinoc = serial.Serial("COM3", 9600, timeout=1)
            print("Se conecto")
        except:
            print("Error con arduino")

    def luces(self, comando):
        if comando == "Cuarto1":
            botonc = self.Cuarto1
        elif comando == "Cuarto2":
            botonc = self.Cuarto2
        elif comando == "Cuarto3":
            botonc = self.Cuarto3
        elif comando == "Cuarto4":
            botonc = self.Cuarto4
        print(comando)
        self.arduinoc.write(comando.encode())
    def mostrar_alerta(self, mensaje):
        alerta = Toplevel(self.casad)
        alerta.title("Casa Domótica - Alerta")
        alerta.geometry("300x150")  # Ajusta el tamaño según tus necesidades
        alerta.resizable(False, False)

        Label(alerta, text=mensaje, fg="red", font=("Helvetica", 12, 'bold')).pack(pady=20)
        Button(alerta, text="Aceptar", command=alerta.destroy).pack(pady=10)
if __name__ == "__main__":
    app = MainScreen([1, 'albertq703@gmail.com', '2024-06-29 12:22:46', 2])
    app.mainloop()
