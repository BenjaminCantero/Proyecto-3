# Crud de ingredientes

from models import Ingrediente
class IngredienteCRUD:
    def __init__(self, session):
        self.session = session

    def crear_ingrediente(self, nombre, tipo, cantidad, unidad):
        nuevo_ingrediente = Ingrediente(nombre=nombre, tipo=tipo, cantidad=cantidad, unidad=unidad)
        self.session.add(nuevo_ingrediente)
        self.session.commit()

    def leer_ingredientes(self):
        return self.session.query(Ingrediente).all()

    def actualizar_ingrediente(self, ingrediente_id, nombre=None, tipo=None, cantidad=None, unidad=None):
        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if ingrediente:
            if nombre:
                ingrediente.nombre = nombre
            if tipo:
                ingrediente.tipo = tipo
            if cantidad is not None:
                ingrediente.cantidad = cantidad
            if unidad:
                ingrediente.unidad = unidad
            self.session.commit()

    def eliminar_ingrediente(self, ingrediente_id):
        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if ingrediente:
            self.session.delete(ingrediente)
            self.session.commit()