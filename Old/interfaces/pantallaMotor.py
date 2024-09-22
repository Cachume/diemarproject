from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

class Motor(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Sistema Proyecto | Motor")
        self.geometry("700x550")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")

        self.x_values = [0]
        self.y_values = [0]

        self.setup_ui()

    def setup_ui(self):
        title_label = Label(self, text="Control de Velocidad del Motor", font=('Arial', 16, 'bold'), bg="#f0f0f0", fg="#333")
        title_label.pack(pady=10)

        fig, self.ax = plt.subplots(figsize=(4, 3))
        self.line, = self.ax.plot(self.x_values, self.y_values, label='Velocidad')
        self.ax.set_title('Velocidad del Motor')
        self.ax.legend()

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(pady=10)
        self.canvas.draw()

        self.scale = Scale(self, from_=0, to=8, orient=HORIZONTAL, length=400, tickinterval=2, bg="#e0e0e0", 
                           troughcolor="#76c7c0", width=15, sliderlength=25, label="Selecciona la velocidad:")
        self.scale.pack(pady=5)

        self.update_button = Button(self, text="Actualizar Velocidad", fg="#fff", bg="#007acc", font=('Arial', 12, 'bold'), 
                                    command=self.actualizar_grafica)
        self.update_button.pack(pady=20)

    def actualizar_grafica(self):
        try:
            nuevo_valor = float(self.scale.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, selecciona un valor válido.")
            return

        self.x_values.append(self.x_values[-1] + 1)
        self.y_values.append(nuevo_valor)
        self.line.set_data(self.x_values, self.y_values)

        self.ax.set_xlim(min(self.x_values), max(self.x_values))
        self.ax.set_ylim(min(self.y_values), max(self.y_values))

        self.canvas.draw()

    def on_closing(self):
        self.destroy()
        sys.exit()

# Uncomment the following lines if you want to run the application standalone
# if __name__ == "__main__":
#     root = Tk()
#     root.withdraw()  # Hide the root window
#     app = Motor()
#     app.mainloop()
