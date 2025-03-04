from sqlalchemy import Column, Integer, Date, Time, ForeignKey, String
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Entrenamiento(Base):
    __tablename__ = 'entrenamiento'

    id = Column(Integer, primary_key=True)
    fecha = Column(String)
    repeticiones = Column(String)
    tiempo = Column(String)

    id_ejercicio = Column(Integer, ForeignKey('ejercicio.id'))
    ejercicio = relationship('Ejercicio')
    
    id_persona = Column(Integer, ForeignKey('persona.id'))
    persona = relationship('Persona')
    