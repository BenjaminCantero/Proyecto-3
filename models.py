# Definicion de los modelos ORM

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

# Tabla intermedia para la relación N:M entre Menu e Ingrediente
menu_ingrediente = Table('menu_ingrediente', Base.metadata,
    Column('menu_id', Integer, ForeignKey('menu.id')),
    Column('ingrediente_id', Integer, ForeignKey('ingrediente.id'))
)

class Cliente(Base):
    __tablename__ = 'cliente'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    email = Column(String)
    fecha_registro = Column(DateTime, default=datetime.datetime.utcnow)
    
    pedidos = relationship("Pedido", back_populates="cliente")

class Ingrediente(Base):
    __tablename__ = 'ingrediente'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    tipo = Column(String)
    cantidad = Column(Float)
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
    fecha_pedido = Column(DateTime, default=datetime.datetime.utcnow)
    total = Column(Float)
    estado = Column(String)
    
    cliente = relationship("Cliente", back_populates="pedidos")