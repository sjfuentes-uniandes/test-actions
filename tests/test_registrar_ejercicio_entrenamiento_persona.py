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

    def test_guardar_entrenamiento_falla_si_campos_vacios(self):
        # Caso 1: No se puede registrar un entrenamiento si hay campos vacíos.

        # Crear y guardar una Persona
        persona_prueba = Persona(
            nombre=self.data_factory.first_name(),
            apellidos=self.data_factory.last_name(),
            talla=1.70,
            peso=70.0,
            edad=25,
            brazo=30.0,
            cintura=80.0,
            pierna=50.0
        )
        self.session.add(persona_prueba)

        # Crear y guardar un Ejercicio
        ejercicio_prueba = Ejercicio(
            nombre="Press de banca",
            descripcion="Ejercicio para pecho",
            calorias=150,
            enlace="https://ejemplo.com/press-banca"
        )
        self.session.add(ejercicio_prueba)

        self.session.commit()

        # Datos fijos
        datos_base = {
            "persona": persona_prueba,
            "ejercicio": ejercicio_prueba,
            "fecha": datetime.strptime("2025-02-10", "%Y-%m-%d").date(),
        }

        # Casos a probar
        casos_prueba = [
            {**datos_base, "repeticiones": None, "tiempo": str(time(0, 5, 30))},  # Repeticiones vacías
            {**datos_base, "repeticiones": 48, "tiempo": None},  # Tiempo vacío
        ]

        for datos_prueba in casos_prueba:
            campo_vacio = "repeticiones" if datos_prueba["repeticiones"] is None else "tiempo"

            mensaje_error = self.logica.validar_crear_editar_entrenamiento(**datos_prueba)

            self.assertNotEqual(mensaje_error, "", f"No se generó error cuando {campo_vacio} está vacío.")
            self.assertIn("El campo", mensaje_error, f"El mensaje de error para {campo_vacio} no es correcto.")

    def test_falla_fecha_futura(self):
        #Caso 2: No se puede registrar un entrenamiento con una fecha futura

        # Crear y guardar una Persona
        persona_prueba = Persona(
            nombre=self.data_factory.first_name(),
            apellidos=self.data_factory.last_name(),
            talla=1.70,
            peso=70.0,
            edad=25,
            brazo=30.0,
            cintura=80.0,
            pierna=50.0
        )
        self.session.add(persona_prueba)

        # Crear y guardar un Ejercicio
        ejercicio_prueba = Ejercicio(
            nombre="Press de banca",
            descripcion="Ejercicio para pecho",
            calorias=150,
            enlace="https://ejemplo.com/press-banca"
        )
        self.session.add(ejercicio_prueba)

        self.session.commit()

        #Crear Entrenamiento con fecha futura
        mañana = (datetime.now().date() + timedelta(days=1)).strftime("%Y-%m-%d")
        entrenamiento2 = {
            "persona": persona_prueba,
            "ejercicio": ejercicio_prueba,
            "fecha": mañana,
            "repeticiones": "48",
            "tiempo": str(time(0, 2, 30))
        }
        mensaje_error = self.logica.validar_crear_editar_entrenamiento(**entrenamiento2)
        self.assertNotEqual(mensaje_error, "", "No se generó error con una fecha futura.")
        self.assertEqual(mensaje_error, "Fecha inválida. Debe ser pasada o actual.", "El mensaje de error no coincide.")

    def test_falla_repeticiones(self):
        #Caso 3-HU012: No se puede registrar un entrenamiento con repeticiones fuera del rango 1-9999 o valores no numéricos

        # Crear y guardar una Persona
        persona_prueba = Persona(
            nombre=self.data_factory.first_name(),
            apellidos=self.data_factory.last_name(),
            talla=1.70,
            peso=70.0,
            edad=25,
            brazo=30.0,
            cintura=80.0,
            pierna=50.0
        )
        self.session.add(persona_prueba)

        # Crear y guardar un Ejercicio
        ejercicio_prueba = Ejercicio(
            nombre="Press de banca",
            descripcion="Ejercicio para pecho",
            calorias=150,
            enlace="https://ejemplo.com/press-banca"
        )
        self.session.add(ejercicio_prueba)

        self.session.commit()

        #Crear Entrenamiento con diferentes casos de repeticiones invalidas
        valores_invalidos = [10000, -5, "abc"]  # Casos inválidos: fuera de rango o no numérico

        for rep in valores_invalidos:
            entrenamiento3 = {
                "persona": persona_prueba,
                "ejercicio": ejercicio_prueba,
                "fecha": datetime.strptime("2025-02-10", "%Y-%m-%d").date(),
                "repeticiones": rep,
                "tiempo": str(time(0, 2, 45))
            }

            mensaje_error = self.logica.validar_crear_editar_entrenamiento(**entrenamiento3)
            
            self.assertNotEqual(mensaje_error, "", f"No se generó error con repeticiones inválidas: {rep}.")
            self.assertEqual(mensaje_error, "Las repeticiones deben ser un número entre 1 y 9999.",
                             f"El mensaje de error no coincide para repeticiones {rep}.")

    def test_dato_tipo_tiempo(self):
    #Caso 4: No se puede registrar un entrenamiento con formato de tiempo diferente a HH:MM:SS

        # Crear y guardar una Persona
        persona_prueba = Persona(
            nombre=self.data_factory.first_name(),
            apellidos=self.data_factory.last_name(),
            talla=1.70,
            peso=70.0,
            edad=25,
            brazo=30.0,
            cintura=80.0,
            pierna=50.0
        )
        self.session.add(persona_prueba)

        # Crear y guardar un Ejercicio
        ejercicio_prueba = Ejercicio(
            nombre="Press de banca",
            descripcion="Ejercicio para pecho",
            calorias=150,
            enlace="https://ejemplo.com/press-banca"
        )
        self.session.add(ejercicio_prueba)

        self.session.commit()


        tiempos = ["12:30", "12:30:45:00", "12:30:45:00:00","::15", "asaaf", "44"]
        for tiempo in tiempos:
            entrenamiento4 = {
                "persona": persona_prueba,
                "ejercicio": ejercicio_prueba,
                "fecha": datetime.strptime("2025-02-10", "%Y-%m-%d").date(),
                "repeticiones": "48",
                "tiempo": tiempo
            }

            mensaje_error = self.logica.validar_crear_editar_entrenamiento(**entrenamiento4)

            self.assertNotEqual(mensaje_error, "", f"No se generó error con formato de tiempo inválido: {tiempo}.")
            self.assertEqual(mensaje_error, "Formato de tiempo inválido. Utilice HH:MM:SS.",
                             f"El mensaje de error no coincide para tiempo {tiempo}.")

    def test_guardar_entrenamiento(self):
        #Caso 5: Se guarda un entrenamiento de forma exitosa

        # Crear y guardar una Persona
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
            nombre="Press de banca",
            descripcion="Ejercicio para pecho",
            calorias=self.data_factory.random_int(5, 50),
            enlace="https://ejemplo.com/press-banca"
        )
        self.session.add(ejercicio_prueba)

        self.session.commit()

        #Entrenamiento
        repeticiones_esperadas = self.data_factory.random_int(1, 9999)
        entrenamiento5 = {
            "persona": persona_prueba,
            "ejercicio": ejercicio_prueba.id,
            "fecha": datetime.now().date().strftime("%Y-%m-%d"),
            "repeticiones": repeticiones_esperadas,
            "tiempo": str(time(0, 5, 30))
        }

        resultado = self.logica.crear_entrenamiento(**entrenamiento5)

        entrenamiento_guardado = self.session.query(Entrenamiento).filter(Entrenamiento.id_persona == persona_prueba.id).first()

        self.assertTrue(resultado["exito"], "El entrenamiento no se guardó correctamente.")
        self.assertIsNotNone(entrenamiento_guardado, "El entrenamiento no fue encontrado en la BD.")
        self.assertEqual(int(entrenamiento_guardado.repeticiones), repeticiones_esperadas, "Las repeticiones guardadas no coinciden.")
        self.assertEqual(entrenamiento_guardado.tiempo, str(time(0, 5, 30)), "El tiempo guardado no coincide.")

    def test_falla_guardar_entrenamiento(self):

        # Crear y guardar una Persona
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
            nombre="Press de banca",
            descripcion="Ejercicio para pecho",
            calorias=self.data_factory.random_int(5, 50),
            enlace="https://ejemplo.com/press-banca"
        )
        self.session.add(ejercicio_prueba)

        self.session.commit()

        #Entrenamiento
        entrenamiento5 = {
            "persona": persona_prueba.id,
            "ejercicio": ejercicio_prueba.id,
            "fecha": datetime.now().date().strftime("%Y-%m-%d"),
            "repeticiones": self.data_factory.random_int(1, 9999),
            "tiempo": str(time(0, 5, 30))
        }

        resultado = self.logica.crear_entrenamiento(**entrenamiento5)

        entrenamiento_guardado = self.session.query(Entrenamiento).filter(Entrenamiento.id_persona == persona_prueba.id).first()

        self.assertFalse(resultado["exito"], "Hubo un error inesperado al guardar el entrenamiento")

    def test_guardar_entrenamiento_con_datos_validos(self):
        #Caso 6: Se valida que un entrenamiento correctamente validado se guarde en la BD sin cambios.
        # Crear y guardar una Persona
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
            nombre="Press de banca",
            descripcion="Ejercicio para pecho",
            calorias=self.data_factory.random_int(5, 50),
            enlace="https://ejemplo.com/press-banca"
        )
        self.session.add(ejercicio_prueba)

        self.session.commit()

        #Entrenamiento
        repeticiones_esperadas = self.data_factory.random_int(1, 9999)
        entrenamiento_prueba = {
            "persona": persona_prueba,
            "ejercicio": ejercicio_prueba,
            "fecha": datetime.now().date().strftime("%Y-%m-%d"),
            "repeticiones": repeticiones_esperadas,
            "tiempo": str(time(0, 5, 30))
        }

        mensaje_error = self.logica.validar_crear_editar_entrenamiento(**entrenamiento_prueba)
        self.assertEqual(mensaje_error, "", f"Hubo un error inesperado en la validación: {mensaje_error}")

        resultado = self.logica.crear_entrenamiento(persona=persona_prueba, ejercicio=ejercicio_prueba.id, fecha=entrenamiento_prueba["fecha"], repeticiones=entrenamiento_prueba["repeticiones"], tiempo=entrenamiento_prueba["tiempo"])

        entrenamiento_guardado = self.session.query(Entrenamiento).filter(Entrenamiento.id_persona == persona_prueba.id).first()

        self.assertIsNotNone(entrenamiento_guardado, "El entrenamiento no fue encontrado en la BD.")
        self.assertEqual(entrenamiento_guardado.fecha, entrenamiento_prueba["fecha"], "La fecha guardada no coincide.")
        self.assertEqual(int(entrenamiento_guardado.repeticiones), entrenamiento_prueba["repeticiones"], "Las repeticiones guardadas no coinciden.")
        self.assertEqual(entrenamiento_guardado.tiempo, entrenamiento_prueba["tiempo"], "El tiempo guardado no coincide.")