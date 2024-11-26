from sqlalchemy.exc import SQLAlchemyError
from models import Pedido  # Asegúrate de que Pedido esté correctamente importado

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

            # Asociar los items al pedido (si tienes un modelo de items relacionado)
            for item in items:
                nuevo_item = Item(
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

    def obtener_todos(self):
        """
        Obtiene todos los pedidos de la base de datos.
        """
        try:
            return self.session.query(Pedido).all()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error al obtener pedidos: {str(e)}")

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
