#Intefaz Grafica proyecto

import customtkinter as ctk
import tkinter as tk

# Configuración de la ventana principal
ctk.set_appearance_mode("dark")  # Modo oscuro de CustomTkinter
ctk.set_default_color_theme("blue")  # Tema de color azul

class RestauranteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Gestión de Restaurante")
        self.geometry("800x600")
        
        # Menú de navegación lateral
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")
        
        # Botones de navegación
        self.btn_ingredientes = ctk.CTkButton(self.sidebar, text="Panel de Ingredientes", command=self.mostrar_panel_ingredientes)
        self.btn_ingredientes.pack(pady=10, padx=20)

        self.btn_menus = ctk.CTkButton(self.sidebar, text="Panel de Menús", command=self.mostrar_panel_menus)
        self.btn_menus.pack(pady=10, padx=20)

        self.btn_clientes = ctk.CTkButton(self.sidebar, text="Panel de Clientes", command=self.mostrar_panel_clientes)
        self.btn_clientes.pack(pady=10, padx=20)

        self.btn_compra = ctk.CTkButton(self.sidebar, text="Panel de Compra", command=self.mostrar_panel_compra)
        self.btn_compra.pack(pady=10, padx=20)

        self.btn_pedidos = ctk.CTkButton(self.sidebar, text="Panel de Pedidos", command=self.mostrar_panel_pedidos)
        self.btn_pedidos.pack(pady=10, padx=20)

        self.btn_graficos = ctk.CTkButton(self.sidebar, text="Panel de Gráficos", command=self.mostrar_panel_graficos)
        self.btn_graficos.pack(pady=10, padx=20)
        
        # Contenedor principal para los paneles
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        
        # Mostrar panel inicial
        self.mostrar_panel_ingredientes()
    
    def mostrar_panel_ingredientes(self):
        self.limpiar_panel()
        label = ctk.CTkLabel(self.main_frame, text="Gestión de Ingredientes", font=("Arial", 16))
        label.pack(pady=10)

        # Ejemplo de campos para añadir ingredientes
        ctk.CTkLabel(self.main_frame, text="Nombre del Ingrediente:").pack(pady=5)
        ctk.CTkEntry(self.main_frame).pack(pady=5)
        ctk.CTkLabel(self.main_frame, text="Tipo:").pack(pady=5)
        ctk.CTkEntry(self.main_frame).pack(pady=5)
        ctk.CTkLabel(self.main_frame, text="Cantidad:").pack(pady=5)
        ctk.CTkEntry(self.main_frame).pack(pady=5)
        ctk.CTkLabel(self.main_frame, text="Unidad de Medida:").pack(pady=5)
        ctk.CTkEntry(self.main_frame).pack(pady=5)
    
    def mostrar_panel_menus(self):
        self.limpiar_panel()
        label = ctk.CTkLabel(self.main_frame, text="Gestión de Menús", font=("Arial", 16))
        label.pack(pady=10)

    def mostrar_panel_clientes(self):
        self.limpiar_panel()
        label = ctk.CTkLabel(self.main_frame, text="Gestión de Clientes", font=("Arial", 16))
        label.pack(pady=10)

    def mostrar_panel_compra(self):
        self.limpiar_panel()
        label = ctk.CTkLabel(self.main_frame, text="Panel de Compra", font=("Arial", 16))
        label.pack(pady=10)

    def mostrar_panel_pedidos(self):
        self.limpiar_panel()
        label = ctk.CTkLabel(self.main_frame, text="Gestión de Pedidos", font=("Arial", 16))
        label.pack(pady=10)

    def mostrar_panel_graficos(self):
        self.limpiar_panel()
        label = ctk.CTkLabel(self.main_frame, text="Gráficos Estadísticos", font=("Arial", 16))
        label.pack(pady=10)

    def limpiar_panel(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Crear y ejecutar la aplicación
app = RestauranteApp()
app.mainloop()
