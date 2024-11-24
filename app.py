import customtkinter as ctk
import tkinter as tk
from tkinter import END
from tkinter import ttk
from tkinter import messagebox
import re
from database import Session
from Crud.cliente_crud import ClienteCRUD
from Crud.ingrediente_crud import IngredienteCRUD 
from Crud.menu_crud import MenuCRUD 
from Crud.pedidos_crud import PedidosCRUD

# Crear una sesión
session = Session()

# Instanciar las clases CRUD
cliente_crud = ClienteCRUD(session)
ingrediente_crud = IngredienteCRUD(session)
menu_crud = MenuCRUD(session)
pedido_crud = PedidosCRUD(session)

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
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        title = ctk.CTkLabel(
            header_frame,
            text="Gestión de Ingredientes",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")

        # Formulario de entrada
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Grid para los campos de entrada
        form_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Campos con labels flotantes
        campos = [
            ("Nombre:", "nombre_entry"),
            ("Tipo:", "tipo_entry"),
            ("Cantidad:", "cantidad_entry"),
            ("Categoría:", "categoria_entry"),
            ("Unidad:", "unidad_entry")
        ]

        for idx, (label_text, entry_name) in enumerate(campos):
            container = ctk.CTkFrame(form_frame, fg_color="transparent")
            container.grid(row=0, column=idx, padx=10, pady=10, sticky="ew")

            label = ctk.CTkLabel(container, text=label_text)
            label.pack(anchor="w", padx=5)

            if label_text == "Unidad:":
                # Menú desplegable para Unidad
                entry = ctk.CTkOptionMenu(
                    container,
                    values=["Litro", "Kilo", "Gramo", "Unidad"],
                    height=35
                )
            elif label_text == "Categoría:":
                # Menú desplegable para Categoría
                entry = ctk.CTkOptionMenu(
                    container,
                    values=["Frutas", "Verduras", "Lácteos", "Granos", "Otros"],
                    height=35
                )
            else:
                # Entrada estándar
                entry = ctk.CTkEntry(
                    container,
                    placeholder_text=label_text.replace(":", ""),
                    height=35
                )
            entry.pack(fill="x", expand=True, padx=5)
            setattr(self, entry_name, entry)
        # Botones de acción
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, columnspan=5, pady=(10, 20), sticky="ew")

                # Botones de acción
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, columnspan=5, pady=(10, 20), sticky="ew")

        add_button = ctk.CTkButton(
            button_frame,
            text="Añadir Ingrediente",
            width=150,
            height=40,
            corner_radius=8
        )
        add_button.configure(command=self.añadir_ingrediente)
        add_button.pack(side="left", padx=5)

        update_button = ctk.CTkButton(
            button_frame,
            text="Actualizar Ingrediente",
            width=150,
            height=40,
            corner_radius=8,
            fg_color="green",
            hover_color="darkgreen"
        )
        update_button.configure(command=self.ActualizarIngrediente)
        update_button.pack(side="left", padx=5)

        delete_button = ctk.CTkButton(
            button_frame,
            text="Eliminar Ingrediente",
            width=150,
            height=40,
            corner_radius=8,
            fg_color="red", 
            hover_color="darkred"
        )
        delete_button.configure(command=self.EliminarIngrediente)
        delete_button.pack(side="left", padx=5)

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
        clear_button.configure(command=self.clear_ingrediente)
        clear_button.pack(side="left", padx=5)

        # Tabla mejorada
        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
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

        columns = ("Nombre", "Tipo", "Cantidad", "Categoría", "Unidad")
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

        # Vincular evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_ingrediente)

        self.Actualizar_Treeview_ingredientes()

    def seleccionar_ingrediente(self, event):
        """
        Evento para mostrar los datos del ingrediente seleccionado en los campos de entrada.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            return

        # Obtener los valores de la fila seleccionada
        item_data = self.tree.item(selected_item[0], "values")

        # Asignar valores a los campos
        self.nombre_entry.delete(0, "end")
        self.nombre_entry.insert(0, item_data[0])

        self.tipo_entry.delete(0, "end")
        self.tipo_entry.insert(0, item_data[1])

        self.cantidad_entry.delete(0, "end")
        self.cantidad_entry.insert(0, item_data[2])

        self.categoria_entry.set(item_data[3])  # Para el OptionMenu
        self.unidad_entry.set(item_data[4])    # Para el OptionMenu

    def limpiar_campos(self):
        """
        Limpia todos los campos de entrada.
        """
        self.nombre_entry.delete(0, "end")
        self.tipo_entry.delete(0, "end")
        self.cantidad_entry.delete(0, "end")
        self.categoria_entry.set("")
        self.unidad_entry.set("")

    def Actualizar_Treeview_ingredientes(self):
        # Limpiar la lista
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar los ingredientes 
        for ingrediente in ingrediente_crud.leer_ingredientes():
            self.tree.insert("", "end", values=(ingrediente.nombre,ingrediente.tipo, ingrediente.cantidad, ingrediente.categoria, ingrediente.unidad))
    
    
    def validacion_numero(self, nombre, numero):
        if numero == "":
            messagebox.showerror(title="Error", message=f"El campo {nombre} no puede estar vacío")
            return False
        
        elif re.match(r"^[0-9]*\.?[0-9]+$", numero) is None:  # Expresión regular para aceptar números enteros y flotantes positivos, no permite el signo negativo
            messagebox.showerror(title="Error", message=f"El campo {nombre} solo acepta números positivos")
            return False

        # Si pasa todas las validaciones
        return True

    def validacion_vacio(self,nombre,valor):
        if valor == "":
            messagebox.showerror(title ="Error", message=f"El campo {nombre} no puede estar vacio")
            return False
        return True
    
    def validacion_email(self, nombre, email):
        # Expresión regular para validar el formato de un correo electrónico
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is None:
            messagebox.showerror(title="Error", message=f"El campo {nombre} debe contener un correo válido")
            return False
        return True
    
    def añadir_ingrediente(self):
        nombre_entry = self.nombre_entry.get()
        tipo = self.tipo_entry.get()
        cantidad = self.cantidad_entry.get()
        categoria = self.categoria_entry.get()
        unidad = self.unidad_entry.get()
        
        campos = {'Nombre':nombre_entry,'Tipo':tipo,'Cantidad':cantidad, 'Categoria':categoria, 'Unidad':unidad}
        for nombre,valor in campos.items():
            result = self.validacion_vacio(nombre,valor)
            if not result:
                return False
        if not self.validacion_numero('Cantidad',cantidad):
            return False
        resultado = ingrediente_crud.crear_ingrediente(nombre_entry, tipo, float(cantidad),categoria, unidad)
        if resultado:
            messagebox.showinfo(title="Éxito", message="Ingrediente añadido exitosamente")
            # Limpiar los Entry después de agregar el ingrediente
            self.nombre_entry.delete(0, END)
            self.tipo_entry.delete(0, END)
            self.cantidad_entry.delete(0, END)
            self.categoria_entry.set("")
            self.unidad_entry.set("")
        else:
            messagebox.showinfo(title="Éxito", message=f"Ingrediente existente, se suma.")
        self.Actualizar_Treeview_ingredientes()
    
    def EliminarIngrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror(title="Error", message="Para eliminar un ingrediente primero debe seleccionarlo en la lista.")
            return
        item = self.tree.item(seleccion)
        nombre=item['values'][0]
        ingrediente_crud.eliminar_ingrediente(1, nombre)
        self.Actualizar_Treeview_ingredientes()
    
    def ActualizarIngrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror(title="Error", message="Para actualizar un ingrediente primero debe seleccionarlo en la lista.")
            return
        item = self.tree.item(seleccion)
        nombre_entry = item['values'][0]
        tipo = self.tipo_entry.get()
        cantidad = self.cantidad_entry.get()
        categoria = self.categoria_entry.get()
        unidad = self.unidad_entry.get()
        contador=0
        contador2=0
        campos = {'Nombre':nombre_entry,'Tipo':tipo,'Cantidad':cantidad, 'Categoria':categoria, 'Unidad':unidad}
        for nombre,valor in campos.items():
            if item['values'][contador] == valor:
                contador2+=1
            contador+=1
            result = self.validacion_vacio(nombre,valor)
            if not result:
                return False
        if contador2==5:
            return False
        if not self.validacion_numero('Cantidad',cantidad):
            return False
        resultado = ingrediente_crud.actualizar_ingrediente(-1,nombre_entry, tipo, float(cantidad),categoria, unidad)
        if resultado:
            messagebox.showinfo(title="Éxito", message="Ingrediente actualizado exitosamente")
            # Limpiar los Entry después de agregar el ingrediente
            self.nombre_entry.delete(0, END)
            self.tipo_entry.delete(0, END)
            self.cantidad_entry.delete(0, END)
            self.categoria_entry.set("")
            self.unidad_entry.set("")
        self.Actualizar_Treeview_ingredientes()
    
    def clear_ingrediente(self):
        """
        Elimina todos los datos de ingredientes de la base de datos
        """
        ingredientes=ingrediente_crud.leer_ingredientes()
        for ingrediente in ingredientes:
            ingrediente_crud.eliminar_ingrediente(ingrediente.id)
        self.Actualizar_Treeview_ingredientes()







    def mostrar_panel_menus(self):
        self.limpiar_panel()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
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
        menu_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # Información básica del menú
        info_frame = ctk.CTkFrame(menu_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        # Nombre del menú
        nombre_label = ctk.CTkLabel(info_frame, text="Nombre del Menú:")
        nombre_label.pack(anchor="w", padx=5)
        self.nombre_entrym = ctk.CTkEntry(info_frame, placeholder_text="Ej: Completo Italiano", width=300)
        self.nombre_entrym.pack(anchor="w", padx=5, pady=(0, 10))
        
        # Descripción
        desc_label = ctk.CTkLabel(info_frame, text="Descripción:")
        desc_label.pack(anchor="w", padx=5)
        self.desc_text = ctk.CTkTextbox(info_frame, height=60, width=400)
        self.desc_text.pack(anchor="w", padx=5, pady=(0, 10))
        
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
        
        available_list = ttk.Treeview(left_frame, height=8, columns=("nombre", "cantidad"), show="headings")
        available_list.heading("nombre", text="Nombre")
        available_list.heading("cantidad", text="Cantidad")
        available_list.pack(fill="x", pady=5)
        
        # Ingredientes seleccionados
        selected_label = ctk.CTkLabel(right_frame, text="Ingredientes Seleccionados")
        selected_label.pack(pady=5)
        
        selected_list = ttk.Treeview(right_frame, height=8, columns=("nombre", "cantidad"), show="headings")
        selected_list.heading("nombre", text="Nombre")
        selected_list.heading("cantidad", text="Cantidad")
        selected_list.pack(fill="x", pady=5)
        
        # Botones de acción
        button_frame = ctk.CTkFrame(menu_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)

        update_btn = ctk.CTkButton(
            button_frame,
            text="Actualizar Menú",
            width=150,
            height=40,
            fg_color="green",
            hover_color="darkgreen"
        )
        update_btn.pack(side="right", padx=10)

        delete_btn = ctk.CTkButton(
            button_frame,
            text="Eliminar Menú",
            width=150,
            height=40,
            fg_color="red",
            hover_color="darkred"
        )
        delete_btn.pack(side="right", padx=10)

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
        # Tabla de visualización de menús
        menus_frame = ctk.CTkFrame(self.main_frame)
        menus_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        table_title = ctk.CTkLabel(
            menus_frame,
            text="Lista de Menús",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        table_title.pack(anchor="w", pady=10)
        
        menus_table = ttk.Treeview(menus_frame, columns=("nombre", "descripcion"), show="headings", height=8)
        menus_table.heading("nombre", text="Nombre")
        menus_table.heading("descripcion", text="Descripción")
        menus_table.pack(fill="both", padx=10, pady=10)
        
        # Botones para actualizar y eliminar
        action_frame = ctk.CTkFrame(menus_frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=10, pady=10)
        
        update_btn = ctk.CTkButton(action_frame, text="Actualizar Menú", width=150)
        update_btn.pack(side="left", padx=10)
        
        delete_btn = ctk.CTkButton(action_frame, text="Eliminar Menú", width=150)
        delete_btn.pack(side="left", padx=10)


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
        
        # Formulario de cliente
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.grid(row=1, column=0, padx=20, pady=(0,20), sticky="ew")
        
        # Campos del formulario
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=20, pady=20)
        
        # Nombre
        nombre_label = ctk.CTkLabel(fields_frame, text="Nombre completo:")
        nombre_label.grid(row=0, column=0, padx=5, pady=(0, 15), sticky="w")
        self.nombre_entryc = ctk.CTkEntry(fields_frame, placeholder_text="Nombre del cliente", width=300)
        self.nombre_entryc.grid(row=0, column=1, padx=5, pady=(0, 15), sticky="w")
        # Email
        email_label = ctk.CTkLabel(fields_frame, text="Correo electrónico:")
        email_label.grid(row=0, column=2, padx=5, pady=(0, 15), sticky="w")
        self.email_entry = ctk.CTkEntry(fields_frame, placeholder_text="email@ejemplo.com", width=300)
        self.email_entry.grid(row=0, column=3, padx=5, pady=(0, 15), sticky="w")

        
        # Botones
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        add_button = ctk.CTkButton(
            button_frame,
            text="Nuevo Cliente",
            width=150,
            height=40,
            corner_radius=8,
        )
        add_button.configure(command=self.añadir_cliente)
        add_button.pack(side="left", padx=5)

        delete_button = ctk.CTkButton(
            button_frame,
            text="Eliminar Cliente",
            width=150,
            height=40,
            corner_radius=8,
            fg_color="red", 
            hover_color="darkred"
        )
        delete_button.configure(command=self.EliminarCliente)
        delete_button.pack(side="left", padx=5)

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
        clear_button.configure(command=self.clear_cliente)
        clear_button.pack(side="left", padx=5)
        
        # Lista de clientes
        list_frame = ctk.CTkFrame(self.main_frame)
        list_frame.grid(row=2, column=0, padx=20, pady=(0,20), sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        # Tabla de clientes
        columns = ("Nombre", "Email", "Fecha Registro")
        self.tree3 = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree3.heading(col, text=col)
            self.tree3.column(col, width=150)
        
        self.tree3.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ctk.CTkScrollbar(list_frame, command=self.tree3.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree3.configure(yscrollcommand=scrollbar.set)
        self.Actualizar_Treeview_clientes()
        # Vincular evento de selección
        self.tree3.bind("<<TreeviewSelect>>", self.seleccionar_ciente)
        
    def clear_cliente(self):
        """
        Elimina todos los datos de ingredientes de la base de datos
        """
        clientes=cliente_crud.leer_clientes()
        for cliente in clientes:
            cliente_crud.eliminar_cliente(cliente.id)
        self.Actualizar_Treeview_clientes()
    
    def seleccionar_ciente(self, event):
        """
        Evento para mostrar los datos del ingrediente seleccionado en los campos de entrada.
        """
        selected_item = self.tree3.selection()
        if not selected_item:
            return

        # Obtener los valores de la fila seleccionada
        item_data = self.tree3.item(selected_item[0], "values")

        # Asignar valores a los campos
        self.nombre_entryc.delete(0, "end")
        self.nombre_entryc.insert(0, item_data[0])

        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, item_data[1])

    def añadir_cliente(self):
        nombre_c = self.nombre_entryc.get()
        email = self.email_entry.get()
        
        campos = {'Nombre':nombre_c,'Correo electronico':email}
        for nombre,valor in campos.items():
            result = self.validacion_vacio(nombre,valor)
            if not result:
                return False
        validar_email=self.validacion_email('Correo electronico',email)
        if not validar_email:
            return False
        resultado = cliente_crud.crear_cliente(nombre_c, email)
        if resultado[0]:
            messagebox.showinfo(title="Éxito", message="Cliente añadido exitosamente")
            # Limpiar los Entry después de agregar el ingrediente
            self.nombre_entryc.delete(0, END)
            self.email_entry.delete(0, END)
            self.Actualizar_Treeview_clientes()
        else:
            if resultado[1]==0: mensaje= f'de nombre {nombre_c}'
            elif resultado[1] == 1: mensaje = f'de correo {email}'
            messagebox.showerror(title="Error", message=f"El cliente {mensaje} ya existe")
        
    def EliminarCliente(self):
        seleccion = self.tree3.selection()
        if not seleccion:
            messagebox.showerror(title="Error", message="Para eliminar un cliente primero debe seleccionarlo en la lista.")
            return
        item = self.tree3.item(seleccion)
        nombre=item['values'][0]
        cliente_crud.eliminar_cliente(-1, nombre)
        self.Actualizar_Treeview_clientes()
    
    def Actualizar_Treeview_clientes(self):
        # Limpiar la lista
        for item in self.tree3.get_children():
            self.tree3.delete(item)

        # Agregar los ingredientes 
        for cliente in cliente_crud.leer_clientes():
            self.tree3.insert("", "end", values=(cliente.nombre,cliente.email,cliente.fecha_registro))
 






    def mostrar_panel_compra(self):
        self.limpiar_panel()

        # Header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        title = ctk.CTkLabel(
            header_frame,
            text="Panel de Compra",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")

        # Panel principal de compra
        compra_frame = ctk.CTkFrame(self.main_frame)
        compra_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

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

        menus_list = ttk.Treeview(menus_frame, columns=("nombre", "precio"), show="headings", height=6)
        menus_list.heading("nombre", text="Nombre")
        menus_list.heading("precio", text="Precio")
        menus_list.pack(fill="x", padx=20, pady=5)

        # Campo para cantidad
        cantidad_frame = ctk.CTkFrame(menus_frame, fg_color="transparent")
        cantidad_frame.pack(fill="x", padx=20, pady=5)

        cantidad_label = ctk.CTkLabel(cantidad_frame, text="Cantidad:")
        cantidad_label.pack(side="left", padx=5)

        cantidad_entry = ctk.CTkEntry(cantidad_frame, width=100)
        cantidad_entry.pack(side="left", padx=5)

        # Botón agregar al carrito
        add_cart_btn = ctk.CTkButton(
            menus_frame,
            text="Agregar al Carrito",
            width=150,
            command=lambda: self.agregar_al_carrito(menus_list, cantidad_entry)
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

        cart_list = ttk.Treeview(cart_frame, columns=("nombre", "cantidad", "precio"), show="headings", height=6)
        cart_list.heading("nombre", text="Nombre")
        cart_list.heading("cantidad", text="Cantidad")
        cart_list.heading("precio", text="Precio")
        cart_list.pack(fill="x", padx=20, pady=5)

        self.cart_list = cart_list  # Guardar referencia para su uso posterior

        # Total y botones de acción
        total_frame = ctk.CTkFrame(compra_frame, fg_color="transparent")
        total_frame.pack(fill="x", padx=20, pady=10)

        self.total_label = ctk.CTkLabel(
            total_frame,
            text="Total: $0.00",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.total_label.pack(side="right", padx=10)

        # Botones finales
        button_frame = ctk.CTkFrame(compra_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=10)

        generar_btn = ctk.CTkButton(
            button_frame,
            text="Generar Pedido",
            width=150,
            height=40,
            command=self.generar_pedido_pdf
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

    # Métodos adicionales
    def agregar_al_carrito(self, menus_list, cantidad_entry):
        try:
            cantidad = int(cantidad_entry.get())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida.")
            return

        seleccion = menus_list.focus()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un menú para agregar.")
            return

        valores = menus_list.item(seleccion, "values")
        nombre, precio = valores[0], float(valores[1])

        self.cart_list.insert("", "end", values=(nombre, cantidad, f"${precio * cantidad:.2f}"))
        self.actualizar_total()

    def actualizar_total(self):
        total = 0
        for item in self.cart_list.get_children():
            total += float(self.cart_list.item(item, "values")[2][1:])  # Extraer el valor sin el símbolo '$'
        self.total_label.configure(text=f"Total: ${total:.2f}")

    def generar_pedido_pdf(self):
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Pedido de Compra", ln=True, align="C")
        pdf.ln(10)

        pdf.cell(50, 10, txt="Nombre", border=1)
        pdf.cell(30, 10, txt="Cantidad", border=1)
        pdf.cell(30, 10, txt="Precio", border=1)
        pdf.ln()

        for item in self.cart_list.get_children():
            nombre, cantidad, precio = self.cart_list.item(item, "values")
            pdf.cell(50, 10, txt=nombre, border=1)
            pdf.cell(30, 10, txt=str(cantidad), border=1)
            pdf.cell(30, 10, txt=precio, border=1)
            pdf.ln()

        pdf.ln(10)
        pdf.cell(50, 10, txt=self.total_label.cget("text"), align="R")

        pdf_file = "pedido.pdf"
        pdf.output(pdf_file)
        messagebox.showinfo("Pedido Generado", f"Pedido guardado como {pdf_file}")

    
    
    
    
    
    
    
    
    def mostrar_panel_pedidos(self):
        self.limpiar_panel()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        title = ctk.CTkLabel(
            header_frame, 
            text="Gestión de Pedidos",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")
        
        # Filtros de búsqueda
        filter_frame = ctk.CTkFrame(self.main_frame)
        filter_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
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
        table_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        # Crear tabla con las columnas requeridas
        columns = ("ID", "Cliente", "Descripción", "Fecha de creación", "Total", "Cantidad de menús")
        pedidos_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
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
            pedidos_tree.heading(col, text=col)
            pedidos_tree.column(col, width=column_widths[col])
        
        pedidos_tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.pedidos_tree = pedidos_tree  # Guardar referencia para uso posterior
        
        # Scrollbar
        scrollbar = ctk.CTkScrollbar(table_frame, command=pedidos_tree.yview)
        scrollbar.pack(side="right", fill="y")
        pedidos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Botón para mostrar detalles
        details_btn = ctk.CTkButton(
            table_frame,
            text="Mostrar Detalles de Pedido",
            width=200,
            command=self.mostrar_detalles_pedido
        )
        details_btn.pack(side="top", pady=10)
        
        # Panel de detalles
        details_frame = ctk.CTkFrame(self.main_frame)
        details_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
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
            height=5
        )
        
        for col in ["Menu", "Cantidad", "Precio", "Subtotal"]:
            details_tree.heading(col, text=col)
            details_tree.column(col, width=150)
        
        details_tree.pack(fill="x", padx=5, pady=5)
        self.details_tree = details_tree  # Guardar referencia para uso posterior

    # Método para mostrar detalles del pedido seleccionado
    def mostrar_detalles_pedido(self):
        seleccion = self.pedidos_tree.focus()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un pedido para mostrar los detalles.")
            return
        
        pedido = self.pedidos_tree.item(seleccion, "values")
        pedido_id = pedido[0]  # Obtener el ID del pedido seleccionado
        
        # Simulación: Recuperar detalles del pedido desde la base de datos o estructura de datos
        detalles = [
            ("Menu 1", 2, "$10.00", "$20.00"),
            ("Menu 2", 1, "$15.00", "$15.00")
        ]  # Reemplazar con datos reales
        
        # Limpiar tabla de detalles y agregar nuevos datos
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)
        
        for detalle in detalles:
            self.details_tree.insert("", "end", values=detalle)










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