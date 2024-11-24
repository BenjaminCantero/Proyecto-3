from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base  # Asegúrate de que `Base` venga de `database.py`

# Tabla intermedia para la relación N:M entre Menu e Ingrediente
menu_ingrediente = Table(
    'menu_ingrediente', Base.metadata,
    Column('menu_id', Integer, ForeignKey('menu.id')),
    Column('ingrediente_id', Integer, ForeignKey('ingrediente.id'))
)

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    pedidos = relationship("Pedido", back_populates="cliente")

class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    tipo = Column(String)
    cantidad = Column(Float)
    categoria = Column(String)
    unidad = Column(String)
    menus = relationship("Menu", secondary=menu_ingrediente, back_populates="ingredientes")

class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    ingredientes = relationship("Ingrediente", secondary=menu_ingrediente, back_populates="menus")

class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    descripcion = Column(String, nullable=False)
    total = Column(Float, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    cantidad_menus = Column(Integer, nullable=False)
    estado = Column(String, nullable=False)
    cliente = relationship("Cliente", back_populates="pedidos")
