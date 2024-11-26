# Creacion de Graficos proyecto
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

class Graficos:
    def __init__(self, graph_frame, pedido_crud, menu_crud, ingrediente_crud):
        self.graph_frame = graph_frame
        self.pedido_crud = pedido_crud
        self.menu_crud = menu_crud
        self.ingrediente_crud = ingrediente_crud
        self.canvas_grafico = None

    def generar_grafico(self, tipo_grafico):
        """
        Genera un gráfico basado en el tipo seleccionado y lo muestra en el frame.
        """
        # Limpiar gráfico anterior si existe
        if self.canvas_grafico:
            self.canvas_grafico.get_tk_widget().destroy()
        
        # Crear nueva figura
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if tipo_grafico == "Ventas Diarias":
            self._grafico_ventas_diarias(ax)
        elif tipo_grafico == "Ventas Mensuales":
            self._grafico_ventas_mensuales(ax)
        elif tipo_grafico == "Menús más Vendidos":
            self._grafico_menus_mas_vendidos(ax)
        elif tipo_grafico == "Ingredientes más Utilizados":
            self._grafico_ingredientes_mas_utilizados(ax)

        # Configurar estilo
        plt.style.use('dark_background')
        fig.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        
        # Crear widget de canvas
        self.canvas_grafico = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas_grafico.draw()
        self.canvas_grafico.get_tk_widget().pack(fill='both', expand=True)

    def _grafico_ventas_diarias(self, ax):
        """
        Genera un gráfico de barras para las ventas diarias.
        """
        fechas = []
        ventas = []
        for i in range(7):  # Últimos 7 días
            fecha = datetime.now() - timedelta(days=i)
            total = self.pedido_crud.obtener_ventas_por_fecha(fecha)
            fechas.append(fecha.strftime('%d/%m'))
            ventas.append(total)
        
        ax.bar(fechas, ventas)
        ax.set_title('Ventas Diarias')

    def _grafico_ventas_mensuales(self, ax):
        """
        Genera un gráfico de línea para las ventas mensuales.
        """
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
        ventas = self.pedido_crud.obtener_ventas_mensuales()
        ax.plot(meses, ventas, marker='o')
        ax.set_title('Ventas Mensuales')

    def _grafico_menus_mas_vendidos(self, ax):
        """
        Genera un gráfico de pastel para los menús más vendidos.
        """
        menus = self.menu_crud.obtener_mas_vendidos()
        nombres = [menu['nombre'] for menu in menus]
        cantidades = [menu['cantidad'] for menu in menus]
        
        ax.pie(cantidades, labels=nombres, autopct='%1.1f%%')
        ax.set_title('Menús más Vendidos')

    def _grafico_ingredientes_mas_utilizados(self, ax):
        """
        Genera un gráfico de barras horizontales para los ingredientes más utilizados.
        """
        ingredientes = self.ingrediente_crud.obtener_mas_utilizados()
        nombres = [ing['nombre'] for ing in ingredientes]
        cantidades = [ing['cantidad'] for ing in ingredientes]
        
        ax.barh(nombres, cantidades)
        ax.set_title('Ingredientes más Utilizados')
