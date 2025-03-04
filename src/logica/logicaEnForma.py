from src.modelo.persona import Persona
from src.modelo.entrenamiento import Entrenamiento
from src.modelo.ejercicio import Ejercicio
from src.logica.FachadaEnForma import FachadaEnForma
from src.modelo.declarative_base import engine, Base, session
from datetime import datetime
from sqlalchemy import collate


class LogicaEnForma(FachadaEnForma):

    def __init__(self):
        Base.metadata.create_all(engine)

        if session.query(Persona).count() == 0:
            print("Populando la base de datos con personas")

            persona1 = Persona(nombre="Carlos", apellidos="Zapata", talla=1.70, peso=70, edad=25, brazo=30, cintura=80, pierna=40, fechaRetiro="")
            persona2 = Persona(nombre="Ana", apellidos="Martínez", talla=1.60, peso=60, edad=30, brazo=25, cintura=70, pierna=35, fechaRetiro="")
            persona3 = Persona(nombre="Alex", apellidos="Noboa", talla=1.75, peso=75, edad=35, brazo=35, cintura=85, pierna=45, fechaRetiro="")
            persona4 = Persona(nombre="Bryan", apellidos="Muñoz", talla=1.50, peso=48, edad=20, brazo=24, cintura=80, pierna=30, fechaRetiro="")
            persona5 = Persona(nombre="Santiago", apellidos="Ríos", talla=1.72, peso=80, edad=15, brazo=15, cintura=90, pierna=42, fechaRetiro="")
            persona6 = Persona(nombre="Daniel", apellidos="Ugarte", talla=1.78, peso=85, edad=21, brazo=20, cintura=75, pierna=48, fechaRetiro="")
            persona7 = Persona(nombre="Diego", apellidos="Garces", talla=1.80, peso=76, edad=56, brazo=23, cintura=86, pierna=38, fechaRetiro="")
            persona8 = Persona(nombre="Juan", apellidos="Zapata", talla=1.83, peso=80, edad=23, brazo=24, cintura=79, pierna=37, fechaRetiro="")
            persona9 = Persona(nombre="Alejandra", apellidos="Tello", talla=1.83, peso=80, edad=23, brazo=24, cintura=79, pierna=37, fechaRetiro="")
            persona10 = Persona(nombre="Alejandra", apellidos="Guzman", talla=1.83, peso=80, edad=23, brazo=24, cintura=79, pierna=37, fechaRetiro="")

            session.add(persona1)
            session.add(persona2)
            session.add(persona3)
            session.add(persona4)
            session.add(persona5)
            session.add(persona6)
            session.add(persona7)
            session.add(persona8)
            session.add(persona9)
            session.add(persona10)

            session.commit()

        else:
            print("La base de datos ya tiene datos")

        
    def dar_personas(self):
        personas = session.query(Persona).order_by(Persona.nombre, Persona.apellidos).all()
        return personas

    def scroll_habilitado(self):
        return True
    
    def validar_crear_editar_entrenamiento(self, persona, ejercicio, fecha, repeticiones, tiempo):
        if not persona or not ejercicio or not fecha or not repeticiones or not tiempo:
            return "El campo no puede estar vacío"
        else:
            try:
                datetime.strptime(tiempo, "%H:%M:%S").time()
            except ValueError:
                return "Formato de tiempo inválido. Utilice HH:MM:SS."
        
            try:
                repeticiones = int(repeticiones)
                if not (1 <= repeticiones <= 9999):
                    return "Las repeticiones deben ser un número entre 1 y 9999."
            except ValueError:
                return "Las repeticiones deben ser un número entre 1 y 9999."
            try: 
                fecha_str = datetime.strptime(fecha, "%Y-%m-%d").date()
                if fecha_str > datetime.now().date():
                    return "Fecha inválida. Debe ser pasada o actual."
            except:
                return "Formato de fecha invalido. Use YY-MM-DD."
        return ""
    
    def crear_entrenamiento(self, persona, ejercicio, fecha, repeticiones, tiempo):
        validacion = self.validar_crear_editar_entrenamiento(persona, ejercicio, fecha, repeticiones, tiempo)
        if validacion == "":
            try:
                persona = self.dar_persona(persona.id)
                ejercicio_seleccionado = session.query(Ejercicio).filter(Ejercicio.nombre == ejercicio).first()
                
                entrenamiento = Entrenamiento(persona=persona, ejercicio=ejercicio_seleccionado, fecha=fecha, repeticiones=repeticiones, tiempo=tiempo)
                session.add(entrenamiento)
                session.commit()
                # session.close()

                return {"exito": True}
            except Exception as e:
                session.rollback()
                return {"exito": False, "mensaje": "Hubo un error inesperado al guardar el entrenamiento"}
        else:
            return "Hubo un error inesperado en la validación: " + validacion

    def dar_persona(self, id_persona):
        persona = session.query(Persona).filter(Persona.id == id_persona).first()
        return persona

    def dar_ejercicios(self, como_diccionario=False):
        ejercicios = session.query(Ejercicio).order_by(Ejercicio.nombre.collate("NOCASE")).all()

        if como_diccionario:
            return [{"nombre": e.nombre, "descripcion": e.descripcion, "calorias": e.calorias, "enlace": e.enlace}
                    for e in ejercicios]

        return ejercicios

    def dar_entrenamientos(self, id_persona):
        persona = self.dar_persona(id_persona)
        entrenamientos = session.query(Entrenamiento).filter(Entrenamiento.id_persona == persona.id).order_by(Entrenamiento.fecha.desc()).all()
        return entrenamientos
    
    def validar_crear_editar_ejercicio(self, nombre, descripcion, enlace, calorias):
        if not nombre or not descripcion or not calorias or not enlace:
            return "Ninguno de los campos puede estar vacio para crear un ejercicio"
        else:
            if len(nombre) > 100:
                return "El campo nombre no puede tener más de 100 caracteres"
            if len(descripcion) > 250:
                return "El campo descripción no puede tener más de 250 caracteres"
            if not ("https://youtube.com/" in enlace or "https://www.youtube.com/" in enlace):
                return "El campo enlance debe contener un enlace de youtube"
            if session.query(Ejercicio).filter(Ejercicio.nombre == nombre).first() is not None:
                return "Ya existe un ejercicio con ese nombre" 
            try:
                cal = int(calorias)
                if not (0 < cal <= 10000):
                    return "El campo calorias debe ser un numero mayor a 0 y menor a 10.000"
            except:
                return "El campo calorias debe ser un numero"
            
        return ""
    
    def crear_ejercicio(self, nombre, descripcion, enlace, calorias):
        validacion = self.validar_crear_editar_ejercicio(nombre, descripcion, enlace, calorias)
        if validacion == "":
            ejercicio = Ejercicio(nombre=nombre, descripcion=descripcion, enlace=enlace, calorias=calorias)
            session.add(ejercicio)
            session.commit()
            # session.close()
            return "Ejercicio guardado con exito"
        else:
            return "Error al guardar el ejercicio. Intente nuevamente."

    def dar_reporte(self, id_persona):
        persona = self.dar_persona(id_persona)
        persona_dic = {
            "nombre": persona.nombre,
            "apellido": persona.apellidos,
            "talla": persona.talla,
            "peso": persona.peso
        }
        entrenamientos = self.dar_entrenamientos(id_persona)
        reporte = {
            "persona": persona.nombre,
            "imc": 0,
            "clasificacion": "clasificacion",
            "entrenamientos": [],
            "total_repeticiones": 0,
            "total_calorias": 0
        }
        # Agrupar entrenamientos por fecha
        entrenamientos_por_fecha = {}
        for entrenamiento in entrenamientos:
            fecha = entrenamiento.fecha
            if fecha not in entrenamientos_por_fecha:
                entrenamientos_por_fecha[fecha] = {
                    "fecha": fecha,
                    "repeticiones": 0,
                    "calorias": 0
                }
            calorias = int(entrenamiento.repeticiones) * int(entrenamiento.ejercicio.calorias)
            
            entrenamientos_por_fecha[fecha]["repeticiones"] += int(entrenamiento.repeticiones)
            entrenamientos_por_fecha[fecha]["calorias"] += calorias

            reporte["total_repeticiones"] += int(entrenamiento.repeticiones)
            reporte["total_calorias"] += calorias

        reporte["entrenamientos"] = list(entrenamientos_por_fecha.values())
        return {'persona': persona_dic, 'estadisticas': reporte}
