from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from zoneinfo import ZoneInfo

Base = declarative_base()

# Tabla intermedia para la relación N:M entre Menu e Ingrediente
menu_ingrediente = Table(
    'menu_ingrediente', Base.metadata,
    Column('menu_id', Integer, ForeignKey('menu.id', ondelete="CASCADE"), primary_key=True),
    Column('ingrediente_id', Integer, ForeignKey('ingrediente.id', ondelete="CASCADE"), primary_key=True)
)

class Cliente(Base):
    __tablename__ = 'cliente'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    fecha_registro = Column(
        DateTime,
        default=lambda: datetime.now(ZoneInfo("America/Santiago")).replace(microsecond=0)
    )
    
    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

class Ingrediente(Base):
    __tablename__ = 'ingrediente'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    tipo = Column(String)
    cantidad = Column(Float)
    categoria = Column(String)
    unidad = Column(String)
    
    menus = relationship("Menu", secondary=menu_ingrediente, back_populates="ingredientes")

class Menu(Base):
    __tablename__ = 'menu'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio = Column(Float, nullable=False)
    
    ingredientes = relationship(
        "Ingrediente",
        secondary=menu_ingrediente,
        back_populates="menus"
    )
    pedidos_items = relationship("PedidoItem", back_populates="menu", cascade="all, delete-orphan")

class Pedido(Base):
    __tablename__ = 'pedido'
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id', ondelete="CASCADE"), nullable=False)
    fecha_pedido = Column(
        DateTime,
        default=lambda: datetime.now(ZoneInfo("America/Santiago")).replace(microsecond=0)
    )
    total = Column(Float, nullable=False)
    estado = Column(String, default="Pendiente", nullable=False)
    
    cliente = relationship("Cliente", back_populates="pedidos")
    items = relationship("PedidoItem", back_populates="pedido", cascade="all, delete-orphan")

class PedidoItem(Base):
    __tablename__ = 'pedido_item'
    
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedido.id', ondelete="CASCADE"), nullable=False)
    menu_id = Column(Integer, ForeignKey('menu.id', ondelete="CASCADE"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    
    pedido = relationship("Pedido", back_populates="items")
    menu = relationship("Menu", back_populates="pedidos_items")
