import unittest
from faker import Faker
from src.modelo.entrenamiento import Entrenamiento
from src.modelo.ejercicio import Ejercicio
from src.modelo.persona import Persona
from src.logica.logicaEnForma import LogicaEnForma
from src.modelo.declarative_base import Session, Base, engine
from datetime import datetime, timedelta, time

class Test_Listar_Entrenamiento(unittest.TestCase):
    def setUp(self):
        self.logica = LogicaEnForma()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.data_factory = Faker()
        Faker.seed(1000)

    def tearDown(self):
        self.session = Session()
        print("\nAntes de limpiar:")
        print("Personas:", self.session.query(Persona).count())
        print("Ejercicios:", self.session.query(Ejercicio).count())
        print("Entrenamientos:", self.session.query(Entrenamiento).count())
        busqueda = self.session.query(Entrenamiento).all()
        for entrenamiento in busqueda:
            self.session.delete(entrenamiento)
        self.session.commit()
        print("\nDespués de limpiar:")
        print("Personas:", self.session.query(Persona).count())
        print("Ejercicios:", self.session.query(Ejercicio).count())
        print("Entrenamientos:", self.session.query(Entrenamiento).count())
        self.session.close()

    def test_dar_persona(self):
        #Caso 1: Retorna una persona
        persona1 = Persona(nombre=self.data_factory.unique.name(), 
                    apellidos=self.data_factory.unique.name(), 
                    talla=self.data_factory.random.uniform(0.0,3.5), 
                    peso=self.data_factory.random_int(0,300), 
                    edad=self.data_factory.random_int(0,300), 
                    brazo=self.data_factory.random_int(0,300), 
                    cintura=self.data_factory.random_int(0,300), 
                    pierna=self.data_factory.random_int(0,300))
        self.session.add(persona1)
        self.session.commit()
        persona = self.logica.dar_persona(persona1.id)
        self.assertEqual(persona1.id, persona.id, "La persona retornada no es la misma que la registrada")
        self.assertEqual(persona1.nombre, persona.nombre, "La persona retornada no tiene el mismo nombre que la registrada")
        self.assertEqual(persona1.apellidos, persona.apellidos, "La persona retornada no tiene el mismo apellido que la registrada")
    
    def test_retorna_lista_ejercicios(self):
        #Caso 2: Retorna una lista de ejercicios
        ejercicio1 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://ejemplo.com/press-banca1",
            calorias=self.data_factory.random_int(5, 50)
        )
        self.session.add(ejercicio1)
        self.session.commit()
        ejercicios = self.logica.dar_ejercicios()
        self.assertGreaterEqual(len(ejercicios), 1, "No se retornaron ejercicios")
        self.assertIsInstance(ejercicios[0], Ejercicio, "El objeto retornado no es de tipo Ejercicio")

    def test_retorna_lista_correcta_ejercicios(self):
        #Caso 3: Retorna una lista correcta de ejercicios
        ejercicio1 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://ejemplo.com/press-banca2",
            calorias=self.data_factory.random_int(5, 50)
        )
        ejercicio2 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://ejemplo.com/press-banca3",
            calorias=self.data_factory.random_int(5, 50)
        )
        ejercicio3 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://ejemplo.com/press-banca4",
            calorias=self.data_factory.random_int(5, 50)
        )
        self.session.add(ejercicio1)
        self.session.add(ejercicio2)
        self.session.add(ejercicio3)
        self.session.commit()
        ejercicios = self.logica.dar_ejercicios()
        nombres_ejercisios = [ejercicio.nombre for ejercicio in ejercicios]
        self.assertIn(ejercicio1.nombre, nombres_ejercisios, "El primer ejercicio no está en la lista")
        self.assertIn(ejercicio2.nombre, nombres_ejercisios, "El segundo ejercicio no está en la lista")
        self.assertIn(ejercicio3.nombre, nombres_ejercisios, "El tercer ejercicio no está en la lista")
    
    def test_lista_entrenamientos_vacia(self):
        #Caso 4: Retorna lista vacía si la persona no registra entrenamientos
        persona1 = Persona(nombre=self.data_factory.unique.name(), 
                           apellidos=self.data_factory.unique.name(), 
                           talla=self.data_factory.random.uniform(0.0,3.5), 
                           peso=self.data_factory.random_int(0,300), 
                           edad=self.data_factory.random_int(0,300), 
                           brazo=self.data_factory.random_int(0,300), 
                           cintura=self.data_factory.random_int(0,300), 
                           pierna=self.data_factory.random_int(0,300))
        self.session.add(persona1)
        self.session.commit()
        persona = self.logica.dar_persona(persona1.id)
        entrenamientos = self.logica.dar_entrenamientos(persona.id)
        self.assertEqual(len(entrenamientos), 0, "La persona no tiene entrenamientos registrados")

    def test_tipo_entrenamiento(self):
        #Caso 5: Retorna lista de entrenamientos
        persona_prueba = Persona(
            nombre=self.data_factory.first_name(),
            apellidos=self.data_factory.last_name(),
            talla=self.data_factory.random.uniform(1.5, 2.0),
            peso=self.data_factory.random_int(50, 100),
            edad=self.data_factory.random_int(18, 60),
            brazo=self.data_factory.random_int(20, 40),
            cintura=self.data_factory.random_int(60, 100),
            pierna=self.data_factory.random_int(30, 50)
        )
        self.session.add(persona_prueba)

        # Crear y guardar un Ejercicio
        ejercicio_prueba = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            calorias=self.data_factory.random_int(5, 50),
            enlace="https://ejemplo.com/press-banca7"
        )
        self.session.add(ejercicio_prueba)

        self.session.commit()

        entrenamiento = {
            "persona": persona_prueba,
            "ejercicio": ejercicio_prueba.id,
            "fecha": datetime.now().date().strftime("%Y-%m-%d"),
            "repeticiones": self.data_factory.random_int(1, 9999),
            "tiempo": str(time(0, 5, 30))
        }
        
        self.logica.crear_entrenamiento(**entrenamiento)

        entrenamientos = self.logica.dar_entrenamientos(persona_prueba.id)

        self.assertGreaterEqual(len(entrenamientos), 1, "La persona tiene entrenamientos registrados")
        self.assertIsInstance(entrenamientos[0], Entrenamiento, "El objeto retornado no es de tipo Entrenamiento")

    def test_entrenamientos_ordenados(self):
        #Caso 6: Lista de entrenamientos ordenados por fecha
        persona_prueba = Persona(
            nombre=self.data_factory.first_name(),
            apellidos=self.data_factory.last_name(),
            talla=self.data_factory.random.uniform(1.5, 2.0),
            peso=self.data_factory.random_int(50, 100),
            edad=self.data_factory.random_int(18, 60),
            brazo=self.data_factory.random_int(20, 40),
            cintura=self.data_factory.random_int(60, 100),
            pierna=self.data_factory.random_int(30, 50)
        )
        self.session.add(persona_prueba)

        ejercicio1 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://ejemplo.com/press-banca8",
            calorias=self.data_factory.random_int(5, 50)
        )
        ejercicio2 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://ejemplo.com/press-banca9",
            calorias=self.data_factory.random_int(5, 50)
        )
        ejercicio3 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://ejemplo.com/press-banca10",
            calorias=self.data_factory.random_int(5, 50)
        )
        self.session.add(ejercicio1)
        self.session.add(ejercicio2)
        self.session.add(ejercicio3)
        self.session.commit()

        entrenamiento1 = {
            "persona": persona_prueba,
            "ejercicio": ejercicio1.id,
            "fecha": datetime.strptime("2025-02-09", "%Y-%m-%d").date(),
            "repeticiones": self.data_factory.random_int(1, 9999),
            "tiempo": str(time(0, 5, 30))
        }
        self.logica.crear_entrenamiento(**entrenamiento1)

        entrenamientos1 = self.logica.dar_entrenamientos(persona_prueba.id)

        entrenamiento2 = {
            "persona": persona_prueba,
            "ejercicio": ejercicio2.id,
            "fecha": datetime.strptime("2024-02-10", "%Y-%m-%d").date(),
            "repeticiones": self.data_factory.random_int(1, 9999),
            "tiempo": str(time(0, 5, 30))
        }
        self.logica.crear_entrenamiento(**entrenamiento2)

        entrenamiento3 = {
            "persona": persona_prueba,
            "ejercicio": ejercicio3.id,
            "fecha": datetime.now().date().strftime("%Y-%m-%d"),
            "repeticiones": self.data_factory.random_int(1, 9999),
            "tiempo": str(time(0, 5, 30))
        }
        self.logica.crear_entrenamiento(**entrenamiento3)

        entrenamientos2 = self.logica.dar_entrenamientos(persona_prueba.id)

        self.assertEqual(entrenamientos1, sorted(entrenamientos1, key=lambda x: x.fecha, reverse=True), "Los entrenamientos no están ordenados por fecha")
        self.assertEqual(entrenamientos2[0].fecha, entrenamiento3['fecha'], "Los entrenamientos no están ordenados por fecha")