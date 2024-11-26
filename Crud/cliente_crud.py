from models import Cliente
class ClienteCRUD:
    def __init__(self, session):
        self.session = session

    def crear_cliente(self, nombre: str, email: str):
        # Comprobar si ya existe un cliente con el mismo nombre o email
        existente = self.session.query(Cliente).filter(
            (Cliente.nombre == nombre) | (Cliente.email == email)
        ).first()
    
        if existente:
            # Retorna un mensaje indicando qué atributo ya está en uso
            if existente.nombre == nombre:
                return [False,0]
            if existente.email == email:
                return [False,1]

        # Crear y guardar el nuevo cliente si no existe
        nuevo_cliente = Cliente(nombre=nombre, email=email)
        self.session.add(nuevo_cliente)
        self.session.commit()
        return [True]

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

    def eliminar_cliente(self, cliente_id:int, nombre:str=None, correo:str=None):
        if cliente_id>-1 : cliente = self.session.query(Cliente).filter(Cliente.id == cliente_id).first()
        else: cliente = self.session.query(Cliente).filter(Cliente.nombre == nombre).first()
        if cliente:
            self.session.delete(cliente)
            self.session.commit()
            return True
        else: False