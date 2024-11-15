import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class RestauranteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración básica de la ventana
        self.title("Sistema de Gestión de Restaurante")
        self.geometry("1024x768")
        
        # Configurar tema oscuro y colores
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Crear el contenedor principal con grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar mejorado
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)  # Espacio flexible al final
        
        # Logo o título del restaurante
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="RESTAURANTE\nGESTIÓN", 
            font=ctk.CTkFont(size=20, weight="bold"),
            pady=20
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        # Botones de navegación mejorados
        self.nav_buttons = []
        nav_items = [
            ("Ingredientes", "mostrar_panel_ingredientes"),
            ("Menús", "mostrar_panel_menus"),
            ("Clientes", "mostrar_panel_clientes"),
            ("Compras", "mostrar_panel_compra"),
            ("Pedidos", "mostrar_panel_pedidos"),
            ("Gráficos", "mostrar_panel_graficos")
        ]
        
        for idx, (text, command) in enumerate(nav_items, start=1):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                height=40,
                corner_radius=8,
                command=getattr(self, command),
                fg_color="transparent",
                hover_color=("gray70", "gray30"),
                anchor="center"
            )
            btn.grid(row=idx, column=0, padx=20, pady=10, sticky="ew")
            self.nav_buttons.append(btn)
        
        # Marco principal con diseño mejorado
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Mostrar panel inicial
        self.mostrar_panel_ingredientes()
        
    def mostrar_panel_ingredientes(self):
        self.limpiar_panel()
        
        # Título del panel
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        
        title = ctk.CTkLabel(
            header_frame, 
            text="Gestión de Ingredientes",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")
        
        # Formulario de entrada
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.grid(row=1, column=0, padx=20, pady=(0,20), sticky="ew")
        
        # Grid para los campos de entrada
        form_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        # Campos con labels flotantes
        campos = [
            ("Nombre:", "nombre_entry"),
            ("Tipo:", "tipo_entry"),
            ("Cantidad:", "cantidad_entry"),
            ("Unidad:", "unidad_entry")
        ]
        
        for idx, (label_text, entry_name) in enumerate(campos):
            container = ctk.CTkFrame(form_frame, fg_color="transparent")
            container.grid(row=0, column=idx, padx=10, pady=10, sticky="ew")
            
            label = ctk.CTkLabel(container, text=label_text)
            label.pack(anchor="w", padx=5)
            
            entry = ctk.CTkEntry(
                container,
                placeholder_text=label_text.replace(":", ""),
                height=35
            )
            entry.pack(fill="x", expand=True, padx=5)
            setattr(self, entry_name, entry)
        
        # Botones de acción
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, columnspan=4, pady=(10,20), sticky="ew")
        
        add_button = ctk.CTkButton(
            button_frame,
            text="Añadir Ingrediente",
            width=200,
            height=40,
            corner_radius=8
        )
        add_button.pack(side="left", padx=10)
        
        clear_button = ctk.CTkButton(
            button_frame,
            text="Limpiar",
            width=100,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            hover_color=("gray70", "gray30")
        )
        clear_button.pack(side="left", padx=10)
        
        # Tabla mejorada
        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.grid(row=2, column=0, padx=20, pady=(0,20), sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure(
            "Custom.Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            borderwidth=0
        )
        style.configure(
            "Custom.Treeview.Heading",
            background="#1f538d",
            foreground="black",
            relief="flat"
        )
        
        columns = ("Nombre", "Tipo", "Cantidad", "Unidad")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            height=10
        )
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=150, anchor="w")
        
        # Scrollbar
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    def mostrar_panel_menus(self):
        self.limpiar_panel()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        
        title = ctk.CTkLabel(
            header_frame, 
            text="Gestión de Menús",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")
        
        # Botón para nuevo menú
        new_menu_btn = ctk.CTkButton(
            header_frame,
            text="+ Nuevo Menú",
            width=120,
            height=35
        )
        new_menu_btn.pack(side="right")
        
        # Panel de creación de menú
        menu_frame = ctk.CTkFrame(self.main_frame)
        menu_frame.grid(row=1, column=0, padx=20, pady=(0,20), sticky="ew")
        
        # Información básica del menú
        info_frame = ctk.CTkFrame(menu_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        # Nombre del menú
        nombre_label = ctk.CTkLabel(info_frame, text="Nombre del Menú:")
        nombre_label.pack(anchor="w", padx=5)
        nombre_entry = ctk.CTkEntry(info_frame, placeholder_text="Ej: Completo Italiano", width=300)
        nombre_entry.pack(anchor="w", padx=5, pady=(0,10))
        
        # Descripción
        desc_label = ctk.CTkLabel(info_frame, text="Descripción:")
        desc_label.pack(anchor="w", padx=5)
        desc_text = ctk.CTkTextbox(info_frame, height=60, width=400)
        desc_text.pack(anchor="w", padx=5, pady=(0,10))
        
        # Selección de ingredientes
        ingredientes_frame = ctk.CTkFrame(menu_frame)
        ingredientes_frame.pack(fill="x", padx=20, pady=10)
        
        # Título de ingredientes
        ing_title = ctk.CTkLabel(
            ingredientes_frame,
            text="Ingredientes del Menú",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        ing_title.pack(pady=10)
        
        # Lista de ingredientes disponibles
        ing_list_frame = ctk.CTkFrame(ingredientes_frame)
        ing_list_frame.pack(fill="x", padx=20, pady=10)
        
        # Dividir en dos columnas
        left_frame = ctk.CTkFrame(ing_list_frame, fg_color="transparent")
        left_frame.pack(side="left", expand=True, fill="both", padx=10)
        
        right_frame = ctk.CTkFrame(ing_list_frame, fg_color="transparent")
        right_frame.pack(side="right", expand=True, fill="both", padx=10)
        
        # Ingredientes disponibles
        available_label = ctk.CTkLabel(left_frame, text="Ingredientes Disponibles")
        available_label.pack(pady=5)
        
        available_list = ttk.Treeview(left_frame, height=8, columns=("cantidad",), show="headings")
        available_list.heading("cantidad", text="Cantidad")
        available_list.pack(fill="x", pady=5)
        
        # Ingredientes seleccionados
        selected_label = ctk.CTkLabel(right_frame, text="Ingredientes Seleccionados")
        selected_label.pack(pady=5)
        
        selected_list = ttk.Treeview(right_frame, height=8, columns=("cantidad",), show="headings")
        selected_list.heading("cantidad", text="Cantidad")
        selected_list.pack(fill="x", pady=5)
        
        # Botones de acción
        button_frame = ctk.CTkFrame(menu_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Guardar Menú",
            width=150,
            height=40
        )
        save_btn.pack(side="right", padx=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            width=100,
            height=40,
            fg_color="transparent",
            border_width=1
        )
        cancel_btn.pack(side="right", padx=10)

    def mostrar_panel_clientes(self):
        self.limpiar_panel()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        
        title = ctk.CTkLabel(
            header_frame, 
            text="Gestión de Clientes",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")
        
        # Botón nuevo cliente
        new_client_btn = ctk.CTkButton(
            header_frame,
            text="+ Nuevo Cliente",
            width=120,
            height=35
        )
        new_client_btn.pack(side="right")
        
        # Formulario de cliente
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.grid(row=1, column=0, padx=20, pady=(0,20), sticky="ew")
        
        # Campos del formulario
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=20, pady=20)
        
        # Nombre
        nombre_label = ctk.CTkLabel(fields_frame, text="Nombre completo:")
        nombre_label.pack(anchor="w", padx=5)
        nombre_entry = ctk.CTkEntry(fields_frame, placeholder_text="Nombre del cliente", width=300)
        nombre_entry.pack(anchor="w", padx=5, pady=(0,15))
        
        # Email
        email_label = ctk.CTkLabel(fields_frame, text="Correo electrónico:")
        email_label.pack(anchor="w", padx=5)
        email_entry = ctk.CTkEntry(fields_frame, placeholder_text="email@ejemplo.com", width=300)
        email_entry.pack(anchor="w", padx=5, pady=(0,15))
        
        # Botones
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Guardar Cliente",
            width=150,
            height=40
        )
        save_btn.pack(side="right", padx=10)
        
        # Lista de clientes
        list_frame = ctk.CTkFrame(self.main_frame)
        list_frame.grid(row=2, column=0, padx=20, pady=(0,20), sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        # Tabla de clientes
        columns = ("Nombre", "Email", "Fecha Registro")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ctk.CTkScrollbar(list_frame, command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

    def mostrar_panel_compra(self):
        self.limpiar_panel()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        
        title = ctk.CTkLabel(
            header_frame, 
            text="Panel de Compra",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")
        
        # Panel principal de compra
        compra_frame = ctk.CTkFrame(self.main_frame)
        compra_frame.grid(row=1, column=0, padx=20, pady=(0,20), sticky="nsew")
        
        # Selección de cliente
        cliente_frame = ctk.CTkFrame(compra_frame, fg_color="transparent")
        cliente_frame.pack(fill="x", padx=20, pady=10)
        
        cliente_label = ctk.CTkLabel(cliente_frame, text="Seleccionar Cliente:")
        cliente_label.pack(side="left", padx=5)
        
        cliente_combo = ttk.Combobox(cliente_frame, width=40)
        cliente_combo.pack(side="left", padx=5)
        
        # Panel de menús
        menus_frame = ctk.CTkFrame(compra_frame)
        menus_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Lista de menús disponibles
        menus_label = ctk.CTkLabel(
            menus_frame,
            text="Menús Disponibles",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        menus_label.pack(pady=10)
        
        menus_list = ttk.Treeview(menus_frame, columns=("precio",), show="headings", height=6)
        menus_list.heading("precio", text="Precio")
        menus_list.pack(fill="x", padx=20, pady=5)
        
        # Botón agregar al carrito
        add_cart_btn = ctk.CTkButton(
            menus_frame,
            text="Agregar al Carrito",
            width=150
        )
        add_cart_btn.pack(pady=10)
        
        # Carrito de compras
        cart_frame = ctk.CTkFrame(compra_frame)
        cart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        cart_label = ctk.CTkLabel(
            cart_frame,
            text="Carrito de Compras",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cart_label.pack(pady=10)
        
        cart_list = ttk.Treeview(cart_frame, columns=("cantidad", "precio"), show="headings", height=6)
        cart_list.heading("cantidad", text="Cantidad")
        cart_list.heading("precio", text="Precio")
        cart_list.pack(fill="x", padx=20, pady=5)
        
        # Total y botones de acción
        total_frame = ctk.CTkFrame(compra_frame, fg_color="transparent")
        total_frame.pack(fill="x", padx=20, pady=10)
        
        total_label = ctk.CTkLabel(
            total_frame,
            text="Total:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        total_label.pack(side="right", padx=10)
        
        # Botones finales
        button_frame = ctk.CTkFrame(compra_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        generar_btn = ctk.CTkButton(
            button_frame,
            text="Generar Pedido",
            width=150,
            height=40
        )
        generar_btn.pack(side="right", padx=10)
        
        cancelar_btn = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            width=100,
            height=40,
            fg_color="transparent",
            border_width=1
        )
        cancelar_btn.pack(side="right", padx=10)


    def mostrar_panel_pedidos(self):
        self.limpiar_panel()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        
        title = ctk.CTkLabel(
            header_frame, 
            text="Gestión de Pedidos",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")
        
        # Filtros de búsqueda
        filter_frame = ctk.CTkFrame(self.main_frame)
        filter_frame.grid(row=1, column=0, padx=20, pady=(0,20), sticky="ew")
        
        # Cliente
        cliente_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        cliente_frame.pack(fill="x", padx=20, pady=10)
        
        cliente_label = ctk.CTkLabel(cliente_frame, text="Cliente:")
        cliente_label.pack(side="left", padx=5)
        
        cliente_combo = ttk.Combobox(cliente_frame, width=40)
        cliente_combo.pack(side="left", padx=5)
        
        # Fechas
        dates_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        dates_frame.pack(fill="x", padx=20, pady=10)
        
        # Fecha inicio
        fecha_inicio_label = ctk.CTkLabel(dates_frame, text="Fecha inicio:")
        fecha_inicio_label.pack(side="left", padx=5)
        
        fecha_inicio_entry = ctk.CTkEntry(dates_frame, width=120)
        fecha_inicio_entry.pack(side="left", padx=5)
        
        # Fecha fin
        fecha_fin_label = ctk.CTkLabel(dates_frame, text="Fecha fin:")
        fecha_fin_label.pack(side="left", padx=20)
        
        fecha_fin_entry = ctk.CTkEntry(dates_frame, width=120)
        fecha_fin_entry.pack(side="left", padx=5)
        
        # Botón buscar
        buscar_btn = ctk.CTkButton(
            dates_frame,
            text="Buscar",
            width=100
        )
        buscar_btn.pack(side="right", padx=20)
        
        # Tabla de pedidos
        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.grid(row=2, column=0, padx=20, pady=(0,20), sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        # Estilo de la tabla
        style = ttk.Style()
        style.configure(
            "Pedidos.Treeview",
            background="#2b2b2b",
            foreground="white",  # Color de las letras en negro
            fieldbackground="#2b2b2b",
            borderwidth=0
        )
        style.configure(
            "Pedidos.Treeview.Heading",
            background="#1f538d",
            foreground="black",
            relief="flat"
        )
        
        # Crear tabla con las columnas requeridas
        columns = ("ID", "Cliente", "Descripción", "Fecha de creación", "Total", "Cantidad de menús")
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Pedidos.Treeview",
            height=15
        )
        
        # Configurar columnas con anchura adecuada
        column_widths = {
            "ID": 80,
            "Cliente": 200,
            "Descripción": 250,
            "Fecha de creación": 150,
            "Total": 120,
            "Cantidad de menús": 150
        }
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=column_widths[col])
        
        tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ctk.CTkScrollbar(table_frame, command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Panel de detalles
        details_frame = ctk.CTkFrame(self.main_frame)
        details_frame.grid(row=3, column=0, padx=20, pady=(0,20), sticky="ew")
        
        details_label = ctk.CTkLabel(
            details_frame,
            text="Detalles del Pedido",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        details_label.pack(pady=10)
        
        # Tabla de detalles
        details_tree = ttk.Treeview(
            details_frame,
            columns=("Menu", "Cantidad", "Precio", "Subtotal"),
            show="headings",
            style="Pedidos.Treeview",
            height=5
        )
        
        for col in ["Menu", "Cantidad", "Precio", "Subtotal"]:
            details_tree.heading(col, text=col)
            details_tree.column(col, width=150)
        
        details_tree.pack(fill="x", padx=5, pady=5)


    def mostrar_panel_graficos(self):
        self.limpiar_panel()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        
        title = ctk.CTkLabel(
            header_frame, 
            text="Gráficos Estadísticos",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")
        
        # Panel de selección
        selection_frame = ctk.CTkFrame(self.main_frame)
        selection_frame.grid(row=1, column=0, padx=20, pady=(0,20), sticky="ew")
        
        # Tipo de gráfico
        graph_type_frame = ctk.CTkFrame(selection_frame, fg_color="transparent")
        graph_type_frame.pack(fill="x", padx=20, pady=10)
        
        graph_label = ctk.CTkLabel(graph_type_frame, text="Tipo de Gráfico:")
        graph_label.pack(side="left", padx=5)
        
        graph_types = ["Ventas Diarias", "Ventas Semanales", "Ventas Mensuales", "Ventas Anuales", 
                    "Menús más Vendidos", "Ingredientes más Utilizados"]
        graph_combo = ttk.Combobox(graph_type_frame, values=graph_types, width=40)
        graph_combo.set("Seleccione un tipo de gráfico")
        graph_combo.pack(side="left", padx=5)
        
        # Período
        period_frame = ctk.CTkFrame(selection_frame, fg_color="transparent")
        period_frame.pack(fill="x", padx=20, pady=10)
        
        # Fecha inicio
        fecha_inicio_label = ctk.CTkLabel(period_frame, text="Desde:")
        fecha_inicio_label.pack(side="left", padx=5)
        
        fecha_inicio_entry = ctk.CTkEntry(period_frame, width=120)
        fecha_inicio_entry.pack(side="left", padx=5)
        
        # Fecha fin
        fecha_fin_label = ctk.CTkLabel(period_frame, text="Hasta:")
        fecha_fin_label.pack(side="left", padx=20)
        
        fecha_fin_entry = ctk.CTkEntry(period_frame, width=120)
        fecha_fin_entry.pack(side="left", padx=5)
        
        # Botón generar
        generar_btn = ctk.CTkButton(
            period_frame,
            text="Generar Gráfico",
            width=120
        )
        generar_btn.pack(side="right", padx=20)
        
        # Marco para el gráfico
        graph_frame = ctk.CTkFrame(self.main_frame)
        graph_frame.grid(row=2, column=0, padx=20, pady=(0,20), sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        # Placeholder para el gráfico
        graph_placeholder = ctk.CTkLabel(
            graph_frame,
            text="El gráfico se mostrará aquí",
            font=ctk.CTkFont(size=16)
        )
        graph_placeholder.pack(expand=True)
        
        # Panel de estadísticas
        stats_frame = ctk.CTkFrame(self.main_frame)
        stats_frame.grid(row=3, column=0, padx=20, pady=(0,20), sticky="ew")
        
        # Título de estadísticas
        stats_label = ctk.CTkLabel(
            stats_frame,
            text="Resumen Estadístico",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        stats_label.pack(pady=10)
        
        # Grid para estadísticas
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=20, pady=10)
        
        # Estadísticas de ejemplo
        stats = [
            ("Total Ventas:", "$0"),
            ("Promedio Diario:", "$0"),
            ("Mejor Día:", "N/A"),
            ("Peor Día:", "N/A")
        ]
        
        for i, (label_text, value) in enumerate(stats):
            container = ctk.CTkFrame(stats_grid, fg_color="transparent")
            container.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="w")
            
            label = ctk.CTkLabel(container, text=label_text, font=ctk.CTkFont(weight="bold"))
            label.pack(side="left", padx=5)
            
            value_label = ctk.CTkLabel(container, text=value)
            value_label.pack(side="left", padx=5)


    def limpiar_panel(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = RestauranteApp()
    app.mainloop()