# Crud de los menus

from models import Menu
class MenuCRUD:
    def __init__(self, session):
        self.session = session

    def crear_menu(self, nombre: str, descripcion: str, precio: float, ingredientes: list):
        nuevo_menu = Menu(nombre=nombre, descripcion=descripcion, precio=precio)  # Asegúrate de que el modelo Menu tenga un campo 'precio'
        self.session.add(nuevo_menu)
        self.session.commit()

    def leer_menus(self):
        return self.session.query(Menu).all()

    def actualizar_menu(self, menu_id:int, nombre:str=None, descripcion:str=None):
        menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
        if menu:
            if nombre:
                menu.nombre = nombre
            if descripcion:
                menu.descripcion = descripcion
            self.session.commit()

    def eliminar_menu(self, menu_id):
        try:
            menu = self.session.query(Menu).filter(Menu.id == menu_id).first()  # Asegúrate de que 'id' sea el nombre correcto del campo
            if menu:
                self.session.delete(menu)  # Eliminar el menú
                self.session.commit()  # Confirmar los cambios
                return True
            else:
                return False  # El menú no existe
        except Exception as e:
            print(f"Error al eliminar el menú: {str(e)}")  # Imprimir el error para depuración
            return False

    def obtener_ingredientes_por_menu(self, nombre_menu):
        # Implementa la lógica para obtener los ingredientes de un menú específico
       pass

    def guardar_menu(self, menu: Menu):
        self.session.add(menu)  # Agregar el nuevo menú a la sesión
        self.session.commit()  # Confirmar los cambios en la base de dato