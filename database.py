#configuracion de base de datos con ORM

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Configuración de la base de datos
DATABASE_URL = 'sqlite:///restaurante.db'  # Cambia a tu base de datos preferida
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)