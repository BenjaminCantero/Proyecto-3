# Crud de ingredientes
from models import Ingrediente

class IngredienteCRUD:
    def __init__(self, session):
        self.session = session

    def crear_ingrediente(self, nombre: str, tipo: str, cantidad: int, unidad: str, categoria: str = "General"):
        # Comprobar si el ingrediente ya existe
        existente = self.session.query(Ingrediente).filter_by(nombre=nombre).first()
        if existente:
            existente.cantidad += cantidad
            return False  # Retorna False si el ingrediente ya existe
    
        # Crear e insertar el nuevo ingrediente
        nuevo_ingrediente = Ingrediente(nombre=nombre, tipo=tipo, cantidad=cantidad, categoria=categoria, unidad=unidad)
        self.session.add(nuevo_ingrediente)
        self.session.commit()
        return True  # Retorna True si se añadió correctamente

    def leer_ingredientes(self):
        return self.session.query(Ingrediente).all()

    def actualizar_ingrediente(self, ingrediente_id: int, nombre: str = None, tipo: str = None, cantidad: int = None, categoria: str = None, unidad: str = None):
        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if ingrediente:
            if nombre:
                ingrediente.nombre = nombre
            if tipo:
                ingrediente.tipo = tipo
            if cantidad is not None:
                ingrediente.cantidad = cantidad
            if categoria:
                ingrediente.categoria = categoria
            if unidad:
                ingrediente.unidad = unidad
            self.session.commit()

    def eliminar_ingrediente(self, ingrediente_id: int):
        ingrediente = self.session.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if ingrediente:
            self.session.delete(ingrediente)
            self.session.commit()
