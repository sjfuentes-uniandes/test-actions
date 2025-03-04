import unittest
from faker import Faker
from datetime import datetime, timedelta, time
from src.modelo.entrenamiento import Entrenamiento
from src.modelo.persona import Persona
from src.modelo.ejercicio import Ejercicio
from src.logica.logicaEnForma import LogicaEnForma
from src.modelo.declarative_base import Session, Base, engine

class Test_Registrar_Ejercicio_Entrenamiento_Persona(unittest.TestCase):
    def setUp(self):
        self.logica = LogicaEnForma()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.data_factory = Faker()
        Faker.seed(1000)

    def tearDown(self):
        self.session.rollback()
        self.session.query(Entrenamiento).delete()
        self.session.query(Ejercicio).delete()
        self.session.query(Persona).delete()
        self.session.commit()
        self.session.close()

    def test_validacion_nombre_vacio(self):
        
        ejercicio_prueba = {
            "nombre": None,
            "descripcion": self.data_factory.sentence(),
            "calorias": self.data_factory.random_int(1, 10000),
            "enlace": self.data_factory.sentence()
        }

        respuesta  = self.logica.validar_crear_editar_ejercicio(**ejercicio_prueba)

        self.assertNotEqual(respuesta, "", "No se generó error cuando el campo nombre esta vacío")

    def test_validacion_descripcion_vacia(self):
        
        ejercicio_prueba = {
            "nombre": self.data_factory.name(),
            "descripcion": None,
            "calorias": self.data_factory.random_int(1, 10000),
            "enlace": self.data_factory.sentence()
        }

        respuesta  = self.logica.validar_crear_editar_ejercicio(**ejercicio_prueba)

        self.assertNotEqual(respuesta, "", "No se generó error cuando el campo descripción esta vacío")

    def test_validacion_calorias_vacia(self):
        
        ejercicio_prueba = {
            "nombre": self.data_factory.name(),
            "descripcion": self.data_factory.sentence(),
            "calorias": None,
            "enlace": self.data_factory.sentence()
        }

        respuesta  = self.logica.validar_crear_editar_ejercicio(**ejercicio_prueba)

        self.assertNotEqual(respuesta, "", "No se generó error cuando el campo calorias esta vacío")

    def test_validacion_enlace_vacia(self):
        
        ejercicio_prueba = {
            "nombre": self.data_factory.name(),
            "descripcion": self.data_factory.sentence(),
            "calorias": self.data_factory.random_int(1, 10000),
            "enlace": None
        }

        respuesta  = self.logica.validar_crear_editar_ejercicio(**ejercicio_prueba)

        self.assertNotEqual(respuesta, "", "No se generó error cuando el campo enlace esta vacío")

    def test_nombre_max_100_caracteres(self):
        
        ejercicio_prueba = {
            "nombre": self.data_factory.paragraph(),
            "descripcion": self.data_factory.sentence(),
            "calorias": self.data_factory.random_int(1, 10000),
            "enlace": self.data_factory.sentence()
        }

        respuesta  = self.logica.validar_crear_editar_ejercicio(**ejercicio_prueba)

        self.assertNotEqual(respuesta, "", "No se generó error cuando el campo nombre tiene más de 100 caracteres")
        self.assertEqual(respuesta, "El campo nombre no puede tener más de 100 caracteres", "No se generó el error esperado")
    
    def test_nombre_max_250_caracteres(self):
        
        ejercicio_prueba = {
            "nombre": self.data_factory.name(),
            "descripcion": "A" * 251,
            "calorias": self.data_factory.random_int(1, 10000),
            "enlace": self.data_factory.sentence()
        }

        respuesta  = self.logica.validar_crear_editar_ejercicio(**ejercicio_prueba)

        self.assertNotEqual(respuesta, "", "No se generó error cuando el campo descripción tiene más de 250 caracteres")
        self.assertEqual(respuesta, "El campo descripción no puede tener más de 250 caracteres", "No se generó el error esperado")

    def test_enlace_youtube(self):
        
        ejercicio_prueba = {
            "nombre": self.data_factory.name(),
            "descripcion": self.data_factory.sentence(),
            "calorias": self.data_factory.random_int(1, 10000),
            "enlace": self.data_factory.sentence()
        }

        respuesta  = self.logica.validar_crear_editar_ejercicio(**ejercicio_prueba)

        self.assertNotEqual(respuesta, "", "No se generó error cuando el enlace no es de youtube")
        self.assertEqual(respuesta, "El campo enlance debe contener un enlace de youtube")

    def test_enlace_youtube_valido(self):
        
        ejercicio_prueba = {
            "nombre": self.data_factory.name(),
            "descripcion": self.data_factory.sentence(),
            "calorias": self.data_factory.random_int(1, 10000),
            "enlace": "https://youtube.com/watch/fasdfasdf"
        }

        respuesta  = self.logica.validar_crear_editar_ejercicio(**ejercicio_prueba)

        self.assertEqual(respuesta, "", "El enlance es correcto")

    def test_calorias_debe_ser_numero(self):
        
        ejercicio_prueba = {
            "nombre": self.data_factory.name(),
            "descripcion": self.data_factory.sentence(),
            "calorias": "avs",
            "enlace": "https://youtube.com/watch/fasdfasdf"
        }

        respuesta  = self.logica.validar_crear_editar_ejercicio(**ejercicio_prueba)

        self.assertNotEqual(respuesta, "", "No se generó error cuando las calorias no son un número")
        self.assertEqual(respuesta, "El campo calorias debe ser un numero")

    def test_calorias_debe_ser_numero_mayor_cero(self):
        
        ejercicio_prueba = {
            "nombre": self.data_factory.name(),
            "descripcion": self.data_factory.sentence(),
            "calorias": -1,
            "enlace": "https://youtube.com/watch/fasdfasdf"
        }

        respuesta  = self.logica.validar_crear_editar_ejercicio(**ejercicio_prueba)

        self.assertNotEqual(respuesta, "", "No se generó error cuando las calorias no son un número menor a 1")
        self.assertEqual(respuesta, "El campo calorias debe ser un numero mayor a 0 y menor a 10.000")

    def test_calorias_debe_ser_numero_menor_10000(self):
        
        ejercicio_prueba = {
            "nombre": self.data_factory.name(),
            "descripcion": self.data_factory.sentence(),
            "calorias": 11000,
            "enlace": "https://youtube.com/watch/fasdfasdf"
        }

        respuesta  = self.logica.validar_crear_editar_ejercicio(**ejercicio_prueba)

        self.assertNotEqual(respuesta, "", "No se generó error cuando las calorias son mayores a 10000")
        self.assertEqual(respuesta, "El campo calorias debe ser un numero mayor a 0 y menor a 10.000")

    def test_guardar_ejercicio(self):
        
        ejercicio_prueba = {
            "nombre": self.data_factory.name(),
            "descripcion": self.data_factory.sentence(),
            "calorias": 20,
            "enlace": "https://youtube.com/watch/fasdfasdf"
        }

        respuesta  = self.logica.crear_ejercicio(**ejercicio_prueba)

        ejercicio_guardado = self.session.query(Ejercicio).filter(Ejercicio.nombre == ejercicio_prueba["nombre"]).first()

        ejercicios_guardados = self.logica.dar_ejercicios()
        print(f"Ejercicios guardados: {len(ejercicios_guardados)}")
        self.assertEqual(respuesta, "Ejercicio guardado con exito")
        self.assertIsNotNone(ejercicio_guardado, "El ejercicio no se guardo correctamente")

    def test_guardar_ejercicio_validado(self):
        
        ejercicio_prueba = {
            "nombre": self.data_factory.name(),
            "descripcion": self.data_factory.sentence(),
            "calorias": self.data_factory.random_int(1, 10000),
            "enlace": self.data_factory.sentence()
        }

        respuesta  = self.logica.crear_ejercicio(**ejercicio_prueba)

        ejercicio_guardado = self.session.query(Ejercicio).filter(Ejercicio.nombre == ejercicio_prueba["nombre"]).first()

        print(respuesta)
        self.assertNotEqual(respuesta, "Ejercicio guardado con exito")
        self.assertIsNone(ejercicio_guardado, "El ejercicio se guardo correctamente")

    def test_ejecicio_duplicado(self):
        ejercicio_prueba1 = {
            "nombre": "Press",
            "descripcion": self.data_factory.sentence(),
            "calorias": self.data_factory.random_int(1, 10000),
            "enlace": "https://youtube.com/watch/fasdfasdf"
        }
        ejercicio_prueba2 = {
            "nombre": "Press",
            "descripcion": self.data_factory.sentence(),
            "calorias": self.data_factory.random_int(1, 10000),
            "enlace": "https://youtube.com/watch/fasdfasdf"
        }

        self.logica.crear_ejercicio(**ejercicio_prueba1)
        respuesta2 = self.logica.crear_ejercicio(**ejercicio_prueba2)

        self.assertEqual(respuesta2, "Error al guardar el ejercicio. Intente nuevamente.")