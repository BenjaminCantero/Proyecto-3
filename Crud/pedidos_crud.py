from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from models import Pedido, PedidoItem  # Asegúrate de que PedidoItem esté correctamente importado

class PedidosCRUD:
    def __init__(self, session):
        self.session = session

    def crear_pedido(self, cliente, descripcion, total, cantidad, items):
        """
        Crea un nuevo pedido y lo guarda en la base de datos.
        """
        try:
            if total < 0:
                raise ValueError("El total no puede ser negativo")

            nuevo_pedido = Pedido(
                cliente=cliente,
                descripcion=descripcion,
                total=total,
                cantidad=cantidad
            )
            self.session.add(nuevo_pedido)
            self.session.commit()

            # Asociar los items al pedido
            for item in items:
                nuevo_item = PedidoItem(
                    pedido_id=nuevo_pedido.id,
                    menu=item["menu"],
                    cantidad=item["cantidad"],
                    precio=item["precio"]
                )
                self.session.add(nuevo_item)
            self.session.commit()

            return nuevo_pedido.id
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Error al crear el pedido: {str(e)}")
        except ValueError as ve:
            raise RuntimeError(str(ve))

    def obtener_todos(self):
        """
        Obtiene todos los pedidos de la base de datos con sus detalles.
        """
        try:
            return self.session.query(Pedido).options(joinedload(Pedido.items)).all()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error al obtener pedidos: {str(e)}")

    def obtener_detalles(self, pedido_id):
        """
        Obtiene los detalles de un pedido específico por su ID.
        """
        try:
            pedido = self.session.query(Pedido).options(joinedload(Pedido.items)).filter(Pedido.id == pedido_id).first()
            if not pedido:
                raise ValueError(f"Pedido con ID {pedido_id} no encontrado")
            detalles = [
                {
                    "menu": item.menu,
                    "cantidad": item.cantidad,
                    "precio": item.precio,
                    "subtotal": item.cantidad * item.precio
                }
                for item in pedido.items
            ]
            return detalles
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error al obtener detalles del pedido: {str(e)}")
        except ValueError as ve:
            raise RuntimeError(str(ve))

    def buscar_por_cliente(self, cliente):
        """
        Busca pedidos filtrados por cliente.
        """
        try:
            return self.session.query(Pedido).filter(Pedido.cliente == cliente).all()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error al filtrar pedidos: {str(e)}")

    def actualizar_cantidad(self, pedido_id, nueva_cantidad):
        """
        Actualiza la cantidad de un pedido.
        """
        try:
            pedido = self.session.query(Pedido).filter(Pedido.id == pedido_id).first()
            if not pedido:
                raise ValueError(f"Pedido con ID {pedido_id} no encontrado")
            if nueva_cantidad < 0:
                raise ValueError("La cantidad no puede ser negativa")
            pedido.cantidad = nueva_cantidad
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Error al actualizar el pedido: {str(e)}")
        except ValueError as ve:
            raise RuntimeError(str(ve))

    def eliminar_pedido(self, pedido_id):
        """
        Elimina un pedido por su ID.
        """
        try:
            pedido = self.session.query(Pedido).filter(Pedido.id == pedido_id).first()
            if not pedido:
                raise ValueError(f"Pedido con ID {pedido_id} no encontrado")
            self.session.delete(pedido)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Error al eliminar el pedido: {str(e)}")
        except ValueError as ve:
            raise RuntimeError(str(ve))
