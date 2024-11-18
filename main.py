from database import Session
from Crud.cliente_crud import ClienteCRUD
from Crud.ingrediente_crud import IngredienteCRUD 
from Crud.menu_crud import MenuCRUD 
from Crud.pedidos_crud import PedidosCRUD

# Crear una sesión
session = Session()

# Instanciar las clases CRUD
cliente_crud = ClienteCRUD(session)
ingrediente_crud = IngredienteCRUD(session)
menu_crud = MenuCRUD(session)
pedido_crud = PedidosCRUD(session)

# Ejemplo de uso
# Crear un nuevo cliente
cliente_crud.crear_cliente("Juan Pérez", "juan@example.com")

# Leer todos los clientes
clientes = cliente_crud.leer_clientes()
print(clientes)

# Crear un nuevo ingrediente
ingrediente_crud.crear_ingrediente("Tomate", "Vegetal", 10, "kg")

# Leer todos los ingredientes
ingredientes = ingrediente_crud.leer_ingredientes()
print(ingredientes)

# Crear un nuevo menú
menu_crud.crear_menu("Ensalada Fresca", "Ensalada con vegetales frescos")

# Leer todos los menús
menus = menu_crud.leer_menus()
print(menus)

# Crear un nuevo pedido
pedido_crud.crear_pedido(cliente_id=1, total=25.50, estado="Pendiente")

# Leer todos los pedidos
pedidos = pedido_crud.leer_pedidos()
print(pedidos)