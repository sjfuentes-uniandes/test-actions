from sqlalchemy import Column, Integer, Date, String, Float
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Persona(Base):
    __tablename__ = 'persona'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellidos = Column(String)
    talla = Column(Float)
    peso = Column(Float)
    edad = Column(Integer)
    brazo = Column(Float)
    cintura = Column(Float)
    pierna = Column(Float)
    fechaRetiro = Column(String, nullable=True)
    razonRetiro = Column(String, nullable=True)

    entrenamientos = relationship('Entrenamiento', cascade='all, delete, delete-orphan')
    