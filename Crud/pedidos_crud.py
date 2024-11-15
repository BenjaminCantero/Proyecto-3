# CRUD de los pedidos

from models import Pedido
class PedidosCRUD:
    def __init__(self, session):
        self.session = session

    def crear_pedido(self, cliente_id, total, estado):
        nuevo_pedido = Pedido(cliente_id=cliente_id, total=total, estado=estado)
        self.session.add(nuevo_pedido)
        self.session.commit()

    def leer_pedidos(self):
        return self.session.query(Pedido).all()

    def actualizar_pedido(self, pedido_id, cliente_id=None, total=None, estado=None):
        pedido = self.session.query(Pedido).filter(Pedido.id == pedido_id).first()
        if pedido:
            if cliente_id:
                pedido.cliente_id = cliente_id
            if total is not None:
                pedido.total = total
            if estado:
                pedido.estado = estado
            self.session.commit()

    def eliminar_pedido(self, pedido_id):
        pedido = self.session.query(Pedido).filter(Pedido.id == pedido_id).first()
        if pedido:
            self.session.delete(pedido)
            self.session.commit()