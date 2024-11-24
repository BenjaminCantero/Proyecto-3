from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ingrediente(Base):
    __tablename__ = 'ingredientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    unidad_medida = Column(String, nullable=False)
    
    __table_args__ = (UniqueConstraint('nombre', 'tipo', name='_nombre_tipo_uc'),)