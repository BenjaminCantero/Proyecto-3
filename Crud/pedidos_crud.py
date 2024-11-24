# CRUD de los pedidos

from models import Pedido
class PedidosCRUD:
    def __init__(self, session):
        self.session = session

    def crear_pedido(self, cliente_id: int, descripcion: str, total: float, cantidad_menus: int, estado: str):
        nuevo_pedido = Pedido(
            cliente_id=cliente_id,
            descripcion=descripcion,
            total=total,
            cantidad_menus=cantidad_menus,
            estado=estado
        )
        self.session.add(nuevo_pedido)
        self.session.commit()

    def leer_pedidos(self):
        return self.session.query(Pedido).all()

    def leer_pedidos_por_cliente(self, cliente_id: int):
        return self.session.query(Pedido).filter(Pedido.cliente_id == cliente_id).all()

    def actualizar_pedido(self, pedido_id: int, cliente_id: int = None, descripcion: str = None, total: float = None, cantidad_menus: int = None, estado: str = None):
        pedido = self.session.query(Pedido).filter(Pedido.id == pedido_id).first()
        if pedido:
            if cliente_id:
                pedido.cliente_id = cliente_id
            if descripcion:
                pedido.descripcion = descripcion
            if total is not None:
                pedido.total = total
            if cantidad_menus is not None:
                pedido.cantidad_menus = cantidad_menus
            if estado:
                pedido.estado = estado
            self.session.commit()

    def eliminar_pedido(self, pedido_id: int):
        pedido = self.session.query(Pedido).filter(Pedido.id == pedido_id).first()
        if pedido:
            self.session.delete(pedido)
            self.session.commit()