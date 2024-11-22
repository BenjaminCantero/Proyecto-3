# Definicion de los modelos ORM

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

Base = declarative_base()

# Tabla intermedia para la relación N:M entre Menu e Ingrediente
menu_ingrediente = Table('menu_ingrediente', Base.metadata,
    Column('menu_id', Integer, ForeignKey('menu.id')),
    Column('ingrediente_id', Integer, ForeignKey('ingrediente.id'))
)

class Cliente(Base):
    __tablename__ = 'cliente'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    email = Column(String, unique=True)
    # Definición de la columna con precisión hasta segundos
    fecha_registro = Column(DateTime, default=lambda: datetime.now(ZoneInfo("America/Santiago")).replace(microsecond=0))
    
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
    __tablename__ = 'pedido'
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    fecha_pedido = Column(DateTime, default=lambda: datetime.now(ZoneInfo("America/Santiago")).replace(microsecond=0))
    total = Column(Float)
    estado = Column(String)
    
    cliente = relationship("Cliente", back_populates="pedidos")