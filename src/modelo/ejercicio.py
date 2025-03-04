from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Ejercicio(Base):
    __tablename__ = 'ejercicio'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    calorias = Column(Integer)
    enlace = Column(String)
    
    entrenamientos = relationship('Entrenamiento')
    