import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# Creacion de Graficos proyecto

class GraficosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Opciones de Visualización de Gráficos")

        self.tipo_grafico = tk.StringVar()
        self.menu_desplegable = ttk.Combobox(root, textvariable=self.tipo_grafico)
        self.menu_desplegable['values'] = ('Ventas por fecha', 'Distribución de menús', 'Uso de ingredientes')
        self.menu_desplegable.grid(column=0, row=0)
        self.menu_desplegable.bind('<<ComboboxSelected>>', self.mostrar_grafico)

    def mostrar_grafico(self, event):
        tipo = self.tipo_grafico.get()
        if tipo == 'Ventas por fecha':
            self.grafico_ventas_por_fecha()
        elif tipo == 'Distribución de menús':
            self.grafico_distribucion_menus()
        elif tipo == 'Uso de ingredientes':
            self.grafico_uso_ingredientes()

    def grafico_ventas_por_fecha(self):
        # Aquí iría el código para generar el gráfico de ventas por fecha
        plt.figure()
        plt.title('Ventas por Fecha')
        # Ejemplo de datos
        fechas = ['2023-01-01', '2023-01-02', '2023-01-03']
        ventas = [100, 150, 200]
        plt.plot(fechas, ventas)
        plt.show()

    def grafico_distribucion_menus(self):
        # Aquí iría el código para generar el gráfico de distribución de menús
        plt.figure()
        plt.title('Distribución de Menús')
        # Ejemplo de datos
        menus = ['Menu 1', 'Menu 2', 'Menu 3']
        cantidades = [50, 30, 20]
        plt.bar(menus, cantidades)
        plt.show()

    def grafico_uso_ingredientes(self):
        # Aquí iría el código para generar el gráfico de uso de ingredientes
        plt.figure()
        plt.title('Uso de Ingredientes')
        # Ejemplo de datos
        ingredientes = ['Ingrediente 1', 'Ingrediente 2', 'Ingrediente 3']
        cantidades = [200, 150, 100]
        plt.bar(ingredientes, cantidades)
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraficosApp(root)
    root.mainloop()
