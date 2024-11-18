# CRUD de Clientes
from models import Cliente
class ClienteCRUD:
    def __init__(self, session):
        self.session = session

    def crear_cliente(self, nombre:str, email:str):
        # Comprobar si el ingrediente ya existe
        existente1 = self.session.query(Cliente).filter_by(nombre=nombre).first()
        existente2 = self.session.query(Cliente).filter_by(email=email).first()
        if existente1 or existente2:
            return False  # Retorna False si el ingrediente ya existe
        nuevo_cliente = Cliente(nombre=nombre, email=email)
        self.session.add(nuevo_cliente)
        self.session.commit()

    def leer_clientes(self):
        return self.session.query(Cliente).all()

    def actualizar_cliente(self, cliente_id:int, nombre:str=None, email:str=None):
        cliente = self.session.query(Cliente).filter(Cliente.id == cliente_id).first()
        if cliente:
            if nombre:
                cliente.nombre = nombre
            if email:
                cliente.email = email
            self.session.commit()

    def eliminar_cliente(self, cliente_id:int):
        cliente = self.session.query(Cliente).filter(Cliente.id == cliente_id).first()
        if cliente:
            self.session.delete(cliente)
            self.session.commit()