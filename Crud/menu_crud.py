# Crud de los menus

from models import Menu
class MenuCRUD:
    def __init__(self, session):
        self.session = session

    def crear_menu(self, nombre, descripcion):
        nuevo_menu = Menu(nombre=nombre, descripcion=descripcion)
        self.session.add(nuevo_menu)
        self.session.commit()

    def leer_menus(self):
        return self.session.query(Menu).all()

    def actualizar_menu(self, menu_id, nombre=None, descripcion=None):
        menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
        if menu:
            if nombre:
                menu.nombre = nombre
            if descripcion:
                menu.descripcion = descripcion
            self.session.commit()

    def eliminar_menu(self, menu_id):
        menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
        if menu:
            self.session.delete(menu)
            self.session.commit()