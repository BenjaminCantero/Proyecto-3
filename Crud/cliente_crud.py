# CRUD de Clientes
from models import Cliente
class ClienteCRUD:
    def __init__(self, session):
        self.session = session

    def crear_cliente(self, nombre, email):
        nuevo_cliente = Cliente(nombre=nombre, email=email)
        self.session.add(nuevo_cliente)
        self.session.commit()

    def leer_clientes(self):
        return self.session.query(Cliente).all()

    def actualizar_cliente(self, cliente_id, nombre=None, email=None):
        cliente = self.session.query(Cliente).filter(Cliente.id == cliente_id).first()
        if cliente:
            if nombre:
                cliente.nombre = nombre
            if email:
                cliente.email = email
            self.session.commit()

    def eliminar_cliente(self, cliente_id):
        cliente = self.session.query(Cliente).filter(Cliente.id == cliente_id).first()
        if cliente:
            self.session.delete(cliente)
            self.session.commit()