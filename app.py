import customtkinter as ctk
import tkinter as tk
from tkinter import END
from tkinter import ttk
from tkinter import messagebox
import re
from database import SessionLocal  # Esto es correcto
from Crud.cliente_crud import ClienteCRUD
from Crud.ingrediente_crud import IngredienteCRUD 
from Crud.menu_crud import MenuCRUD 
from Crud.pedidos_crud import PedidosCRUD

# Crear una sesión
session = SessionLocal()

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
            command=self.crear_nuevo_menu
        )
        new_menu_btn.pack(side="right")
        
        # Botón para eliminar menú
        delete_menu_btn = ctk.CTkButton(
            header_frame,
            text="- Eliminar Menú",
            width=120,
            command=self.eliminar_menu
        )
        delete_menu_btn.pack(side="right")
        
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

        # Precio
        precio_label = ctk.CTkLabel(info_frame, text="Precio:")
        precio_label.pack(anchor="w", padx=5)
        self.precio_entry = ctk.CTkEntry(info_frame, placeholder_text="Ej: 10.99", width=100)
        self.precio_entry.pack(anchor="w", padx=5, pady=(0, 10))

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
        
        self.available_list = ttk.Treeview(left_frame, height= 8, columns=("nombre", "cantidad"), show="headings")
        self.available_list.heading("nombre", text="Nombre")
        self.available_list.heading("cantidad", text="Cantidad")
        self.available_list.pack(fill="x", pady=5)
        
        # Cargar ingredientes disponibles en la lista
        self.cargar_ingredientes_disponibles()
        
        # Ingredientes seleccionados
        selected_label = ctk.CTkLabel(right_frame, text="Ingredientes Seleccionados")
        selected_label.pack(pady=5)
        
        self.selected_list = ttk.Treeview(right_frame, height=8, columns=("nombre", "cantidad"), show="headings")
        self.selected_list.heading("nombre", text="Nombre")
        self.selected_list.heading("cantidad", text="Cantidad")
        self.selected_list.pack(fill="x", pady=5)
        
        # Lista de menús
        menus_frame = ctk.CTkFrame(menu_frame)
        menus_frame.pack(fill="x", padx=20, pady=10)
        
        menus_label = ctk.CTkLabel(menus_frame, text="Menús Disponibles")
        menus_label.pack(pady=5)
        
        self.menus_list = ttk.Treeview(menus_frame, height=8, columns=("nombre", "descripcion", "precio"), show="headings")
        self.menus_list.heading("nombre", text="Nombre")
        self.menus_list.heading("descripcion", text="Descripción")
        self.menus_list.heading("precio", text="Precio")
        self.menus_list.pack(fill="x", pady=5)
        
        # Cargar menús disponibles en la lista
        self.cargar_menus_disponibles()
        
        # Botones de acción
        button_frame = ctk.CTkFrame(menu_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        # Botón agregar ingrediente
        add_ing_btn = ctk.CTkButton(
            button_frame,
            text="Agregar Ingrediente",
            width=150,
            command=self.agregar_ingrediente
        )
        add_ing_btn.pack(side="left", padx=10)
        
        # Botón quitar ingrediente
        remove_ing_btn = ctk.CTkButton(
            button_frame,
            text="Quitar Ingrediente",
            width=150,
            command=self.quitar_ingrediente
        )
        remove_ing_btn.pack(side="left", padx=10)
        
        # Botón guardar menú
        save_menu_btn = ctk.CTkButton(
            button_frame,
            text="Guardar Menú",
            width=150,
            command=self.guardar_menu
        )
        save_menu_btn.pack(side="right", padx=10)
            

    def cargar_ingredientes_disponibles(self):
        # Obtener ingredientes disponibles desde la base de datos
        ingredientes = ingrediente_crud.leer_ingredientes()

        # Limpiar la lista
        for item in self.available_list.get_children():
            self.available_list.delete(item)

        # Agregar ingredientes a la lista
        for ingrediente in ingredientes:
            self.available_list.insert("", "end", values=(ingrediente.nombre, ingrediente.cantidad))

    def agregar_ingrediente(self):
        # Obtener el ingrediente seleccionado de la lista de ingredientes disponibles
        seleccion = self.available_list.focus()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un ingrediente para agregar.")
            return

        # Obtener los valores del ingrediente seleccionado
        ingrediente = self.available_list.item(seleccion, "values")
        nombre_ingrediente = ingrediente[0]
        cantidad_ingrediente = 1  # Puedes permitir que el usuario seleccione la cantidad

        # Verificar si el ingrediente ya está en la lista de ingredientes seleccionados
        for item in self.selected_list.get_children():
            if self.selected_list.item(item, "values")[0] == nombre_ingrediente:
                messagebox.showwarning("Advertencia", f"El ingrediente '{nombre_ingrediente}' ya está en la lista de seleccionados.")
                return

        # Agregar el ingrediente a la lista de ingredientes seleccionados
        self.selected_list.insert("", "end", values=(nombre_ingrediente, cantidad_ingrediente))

    def quitar_ingrediente(self):
        seleccion = self.selected_list.focus()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un ingrediente para quitar.")
            return

        # Eliminar el ingrediente seleccionado de la lista
        self.selected_list.delete(seleccion)


    def crear_nuevo_menu(self):
        # Limpiar los campos de entrada
        self.nombre_entrym.delete(0, "end")
        self.desc_text.delete("1.0", "end")
        
        # Limpiar la lista de ingredientes seleccionados
        for item in self.selected_list.get_children():
            self.selected_list.delete(item)

        # Opcional: Puedes cargar los ingredientes disponibles nuevamente si es necesario
        self.cargar_ingredientes_disponibles()


    def guardar_menu(self):
        # Obtener información del menú
        nombre = self.nombre_entrym.get()
        descripcion = self.desc_text.get("1.0", "end-1c")
        
        # Obtener el precio
        precio_str = self.precio_entry.get()
        try:
            precio = float(precio_str)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return

        # Validar que los campos no estén vacíos
        if not nombre or not descripcion or not precio_str:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        # Obtener ingredientes seleccionados
        selected_ingredients = []
        for item in self.selected_list.get_children():
            ingrediente = self.selected_list.item(item, "values")
            selected_ingredients.append((ingrediente[0], ingrediente[1]))  # (nombre, cantidad)

        # Guardar menú en la base de datos
        try:
            menu_crud.crear_menu(nombre, descripcion, precio, selected_ingredients)
            # Mostrar mensaje de éxito
            messagebox.showinfo("Menú Guardado", "El menú ha sido guardado exitosamente.")
            
            # Limpiar campos
            self.nombre_entrym.delete(0, "end")
            self.desc_text.delete("1.0", "end")
            self.precio_entry.delete(0, "end")
            
            # Opcional: Actualizar la lista de menús disponibles
            self.cargar_menus_disponibles()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el menú. Error: {str(e)}")

    def eliminar_menu(self):
        seleccion = self.menus_list.focus()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un menú para eliminar.")
            return

        # Obtener el ID del menú seleccionado
        menu_id = self.menus_list.item(seleccion, "values")[0]  # Asegúrate de que el ID esté en la primera posición

        # Confirmar la eliminación
        confirmacion = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este menú?")
        if not confirmacion:
            return

        # Llamar a la función de eliminación en el CRUD
        resultado = menu_crud.eliminar_menu(menu_id)

        if resultado:  # Verifica si la eliminación fue exitosa
            self.menus_list.delete(seleccion)  # Eliminar el menú de la lista
            messagebox.showinfo("Menú Eliminado", "El menú ha sido eliminado exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo eliminar el menú. Verifique que exista en la base de datos.")



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

        self.cliente_combo = ttk.Combobox(cliente_frame, width=40)
        self.cliente_combo.pack(side="left", padx=5)

        # Cargar clientes en el combo
        self.cargar_clientes()

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

        self.menus_list = ttk.Treeview(menus_frame, columns=("nombre", "precio"), show="headings", height=6)
        self.menus_list.heading("nombre", text="Nombre")
        self.menus_list.heading("precio", text="Precio")
        self.menus_list.pack(fill="x", padx=20, pady=5)

        # Cargar menús disponibles
        self.cargar_menus_disponibles()

        # Campo para cantidad
        cantidad_frame = ctk.CTkFrame(menus_frame, fg_color="transparent")
        cantidad_frame.pack(fill="x", padx=20, pady=5)

        cantidad_label = ctk.CTkLabel(cantidad_frame, text="Cantidad:")
        cantidad_label.pack(side="left", padx=5)

        self.cantidad_entry = ctk.CTkEntry(cantidad_frame, width=100)
        self.cantidad_entry.pack(side="left", padx=5)

        # Botón agregar al carrito
        add_cart_btn = ctk.CTkButton(
            menus_frame,
            text="Agregar al Carrito",
            width=150,
            command=lambda: self.agregar_al_carrito(self.menus_list, self.cantidad_entry)  # Pasar los argumentos necesarios
        )
        add_cart_btn.pack(pady =10)

        # Carrito de compras
        cart_frame = ctk.CTkFrame(compra_frame)
        cart_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cart_label = ctk.CTkLabel(
            cart_frame,
            text="Carrito de Compras",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cart_label.pack(pady=10)

        self.cart_list = ttk.Treeview(cart_frame, columns=("nombre", "cantidad", "precio"), show="headings", height=6)
        self.cart_list.heading("nombre", text="Nombre")
        self.cart_list.heading("cantidad", text="Cantidad")
        self.cart_list.heading("precio", text="Precio")
        self.cart_list.pack(fill="x", padx=20, pady=5)

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
            command=self.generar_pedido
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

    def cargar_clientes(self):
        # Obtener clientes desde la base de datos
        clientes = cliente_crud.leer_clientes()
        self.cliente_combo['values'] = [cliente.nombre for cliente in clientes]

    def cargar_menus_disponibles(self):
        # Obtener menús disponibles desde la base de datos
        menus = menu_crud.leer_menus()
        for menu in menus:
            self.menus_list.insert("", "end", values=(menu.nombre, menu.precio))

    def agregar_al_carrito(self, menus_list, cantidad_entry):
        # Intentar convertir la entrada de cantidad a un entero
        try:
            cantidad = int(cantidad_entry.get())
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")
        except ValueError as e:
            messagebox.showerror("Error", f"Ingrese una cantidad válida. {str(e)}")
            return

        # Obtener el elemento seleccionado en menus_list
        seleccion = menus_list.focus()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un menú para agregar.")
            return

        # Obtener los valores del elemento seleccionado
        valores = menus_list.item(seleccion, "values")
        if not valores or len(valores) < 2:
            messagebox.showerror("Error", "No se pudo obtener la información del menú seleccionado.")
            return

        # Verificar que el precio sea un valor válido
        try:
            nombre, precio = valores[0], float(valores[1])
        except (ValueError, TypeError) as e:
            messagebox.showerror("Error", "El precio del menú seleccionado no es válido.")
            return

        # Insertar el artículo en el carrito
        self.cart_list.insert("", "end", values=(nombre, cantidad, f"${precio * cantidad:.2f}"))
        
        # Actualizar el total del carrito
        self.actualizar_total()

    def actualizar_total(self):
        total = 0
        for item in self.cart_list.get_children():
            total += float(self.cart_list.item(item, "values")[2][1:])  # Extraer el valor sin el símbolo '$'
        self.total_label.configure(text=f"Total: ${total:.2f}")

    def generar_pedido(self):
        cliente_seleccionado = self.cliente_combo.get()
        if not cliente_seleccionado:
            messagebox.showerror("Error", "Seleccione un cliente para realizar el pedido.")
            return

        # Aquí puedes agregar la lógica para guardar el pedido en la base de datos
        # y disminuir la cantidad de ingredientes necesarios.

        messagebox.showinfo("Pedido Generado", "El pedido ha sido generado exitosamente.")
        self.limpiar_carrito()

    def limpiar_carrito(self):
        self.cart_list.delete(*self.cart_list.get_children())
        self.total_label.configure(text="Total: $0.00")
        self.cantidad_entry.delete(0, "end")

    def generar_pedido(self):
        cliente_seleccionado = self.cliente_combo.get()
        if not cliente_seleccionado:
            messagebox.showerror("Error", "Seleccione un cliente para realizar el pedido.")
            return

        # Obtener los ingredientes del carrito
        for item in self.cart_list.get_children():
            nombre_menu, cantidad, _ = self.cart_list.item(item, "values")
            # Obtener los ingredientes del menú
            ingredientes = menu_crud.obtener_ingredientes_por_menu(nombre_menu)
            
            for ingrediente in ingredientes:
                # Disminuir la cantidad del ingrediente
                ingrediente_crud.disminuir_ingrediente(ingrediente.nombre, ingrediente.cantidad * cantidad)

        messagebox.showinfo("Pedido Generado", "El pedido ha sido generado exitosamente.")
        self.limpiar_carrito()
    













    # Métodos adicionales
    def agregar_al_carrito(self, menus_list, cantidad_entry):
        # Intentar convertir la entrada de cantidad a un entero
        try:
            cantidad = int(cantidad_entry.get())
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")
        except ValueError as e:
            messagebox.showerror("Error", f"Ingrese una cantidad válida. {str(e)}")
            return

        # Obtener el elemento seleccionado en menus_list
        seleccion = menus_list.focus()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un menú para agregar.")
            return

        # Obtener los valores del elemento seleccionado
        valores = menus_list.item(seleccion, "values")
        if not valores or len(valores) < 2:
            messagebox.showerror("Error", "No se pudo obtener la información del menú seleccionado.")
            return

        nombre, precio = valores[0], float(valores[1])

        # Insertar el artículo en el carrito
        self.cart_list.insert("", "end", values=(nombre, cantidad, f"${precio * cantidad:.2f}"))
        
        # Actualizar el total del carrito
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