from models import Menu, Ingrediente, menu_ingrediente

from sqlalchemy.orm import joinedload

class MenuCRUD:
    def __init__(self, session):
        self.session = session

    # Crear un menú con ingredientes
    def crear_menu(self, nombre: str, descripcion: str, precio: float, ingredientes: list):
        try:
            # Crear una instancia del menú
            nuevo_menu = Menu(nombre=nombre, descripcion=descripcion, precio=precio)

            # Vincular los ingredientes al menú
            for ingrediente in ingredientes:
                ingrediente_existente = self.session.query(Ingrediente).filter_by(nombre=ingrediente['nombre']).first()
                if ingrediente_existente:
                    nuevo_menu.ingredientes.append(ingrediente_existente)
                else:
                    nuevo_ingrediente = Ingrediente(
                        nombre=ingrediente['nombre'], 
                        cantidad=ingrediente.get('cantidad', 0)
                    )
                    self.session.add(nuevo_ingrediente)
                    nuevo_menu.ingredientes.append(nuevo_ingrediente)

            self.session.add(nuevo_menu)
            self.session.commit()
            print(f"Menú '{nombre}' creado con éxito.")
        except Exception as e:
            self.session.rollback()
            print(f"Error al crear el menú: {str(e)}")

    # Leer todos los menús
    def leer_menus(self):
        try:
            return self.session.query(Menu).options(joinedload(Menu.ingredientes)).all()
        except Exception as e:
            print(f"Error al leer los menús: {str(e)}")
            return []

    # Actualizar un menú
    def actualizar_menu(self, menu_id: int, nombre: str = None, descripcion: str = None, precio: float = None):
        try:
            menu = self.session.query(Menu).filter_by(id=menu_id).first()
            if not menu:
                print("El menú no existe.")
                return False

            if nombre:
                menu.nombre = nombre
            if descripcion:
                menu.descripcion = descripcion
            if precio:
                menu.precio = precio

            self.session.commit()
            print(f"Menú '{menu_id}' actualizado con éxito.")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al actualizar el menú: {str(e)}")
            return False

    # Eliminar un menú
    def eliminar_menu(self, menu_id: int):
        try:
            menu = self.session.query(Menu).filter_by(id=menu_id).first()
            if not menu:
                print("El menú no existe.")
                return False

            self.session.delete(menu)
            self.session.commit()
            print(f"Menú '{menu_id}' eliminado con éxito.")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al eliminar el menú: {str(e)}")
            return False

    # Obtener ingredientes de un menú
    def obtener_ingredientes_por_menu(self, nombre_menu: str):
        try:
            menu = self.session.query(Menu).filter_by(nombre=nombre_menu).options(joinedload(Menu.ingredientes)).first()
            if not menu:
                print(f"Menú '{nombre_menu}' no encontrado.")
                return []

            return [{"nombre": ingrediente.nombre, "cantidad": ingrediente.cantidad} for ingrediente in menu.ingredientes]
        except Exception as e:
            print(f"Error al obtener ingredientes del menú '{nombre_menu}': {str(e)}")
            return []
