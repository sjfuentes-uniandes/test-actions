import unittest
from faker import Faker
from datetime import datetime, time
from src.logica.logicaEnForma import LogicaEnForma
from src.modelo.declarative_base import Session, Base, engine
from src.modelo.persona import Persona
from src.modelo.ejercicio import Ejercicio

class Test_Ver_Reporte(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.logica = LogicaEnForma()
        self.session = Session()
        self.data_factory = Faker()
        Faker.seed(1000)
        # print('\n--- Nueva prueba ---')

    def tearDown(self):
        self.session.rollback()
        self.session.query(Ejercicio).delete()
        self.session.query(Persona).delete()
        self.session.commit()
        self.session.close()

    def test_no_responde_None(self):
        #Caso 1: El reporte tiene información
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
        # print(f'Persona creada: {persona1.id} - {persona1.nombre}')

        resultado = self.logica.dar_reporte(persona1.id)
        # print(f'Resultado: {resultado}')
        self.assertIsNotNone(resultado, "El reporte responde None")


    def test_reporte_trae_datos_persona(self):
        #Caso 2: El reporte muestra trae o llama los datos de Persona
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
        # print(f'Persona creada: {persona1.id} - {persona1.nombre}')
        resultado = self.logica.dar_reporte(persona1.id)
        # print(f'Resultado: {resultado}')
        self.assertIn('persona', resultado, "El reporte no trae datos de Persona")

    def test_reporte_talla_peso(self):
        #Caso 3: El reporte muestra talla y peso de Persona
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
        # print(f'Persona creada: {persona1.id} - {persona1.nombre}')
        resultado = self.logica.dar_reporte(persona1.id)
        # print(f'Resultado: {resultado}')
        self.assertEqual(resultado["persona"]["talla"], persona1.talla, "Esta no es la altura o talla de la persona")
        self.assertEqual(resultado["persona"]["peso"], persona1.peso, "Este no es el peso de la persona")

    def test_entrenamientos_agrupados_fecha(self):
        # Caso 4: El reporte agrupa los entrenamientos por fecha

        # print(f'Personas antes de prueba: {len(self.logica.dar_personas())}')
        # print(f'Ejercicios antes de prueba: {len(self.logica.dar_ejercicios())}')
        # for persona in self.logica.dar_personas():
        #     print(f'Entrenamietos antes de prueba: {len(self.logica.dar_entrenamientos(persona.id))}')

        persona1 = Persona(nombre=self.data_factory.unique.name(),
                           apellidos=self.data_factory.unique.name(),
                           talla=self.data_factory.random.uniform(0.0, 3.5),
                           peso=self.data_factory.random_int(0, 300),
                           edad=self.data_factory.random_int(0, 300),
                           brazo=self.data_factory.random_int(0, 300),
                           cintura=self.data_factory.random_int(0, 300),
                           pierna=self.data_factory.random_int(0, 300))
        self.session.add(persona1)
        self.session.commit()
        print(f'\n--Caso 4--')
        print(f'\n--Nueva Persona--')
        print(f'Persona creada: {persona1.id} - {persona1.nombre}')
        # print(f'Personas en BD después de crear Persona: {len(self.logica.dar_personas())}')

        # Crear ejercicios
        ejercicio1 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://youtube.com/watch?v=test1",
            calorias=self.data_factory.random_int(5, 50)
        )
        self.session.add(ejercicio1)
        self.session.commit()
        print(f'\n--Nuevo Ejercicio--')
        print(f'Ejercicio creado: {ejercicio1.id} - {ejercicio1.nombre}')
        # print(f'Ejercicios en BD después de prueba: {len(self.logica.dar_ejercicios())}')

        #Crear entrenamientos usando las fechas de prueba
        fecha1 = datetime.now().date().strftime("%Y-%m-%d")

        entrenamiento1 = {
            "persona": persona1,
            "ejercicio": ejercicio1.nombre,
            "fecha": fecha1,
            "repeticiones": self.data_factory.random_int(1, 9999),
            "tiempo": str(time(0, 5, 30))
        }
        validacion1 = self.logica.validar_crear_editar_entrenamiento(**entrenamiento1)
        print(validacion1)
        resultado1 = self.logica.crear_entrenamiento(**entrenamiento1)
        print(f'Resultado: {resultado1}')

        entrenamiento2 = {
            "persona": persona1,
            "ejercicio": ejercicio1.nombre,
            "fecha": fecha1,
            "repeticiones": self.data_factory.random_int(1, 9999),
            "tiempo": str(time(0, 5, 30))
        }
        validacion2 = self.logica.validar_crear_editar_entrenamiento(**entrenamiento2)
        print(validacion2)
        resultado2 = self.logica.crear_entrenamiento(**entrenamiento2)
        print(f'Resultado: {resultado2}')
        # for persona in self.logica.dar_personas():
        #     print(f'Entrenamietos antes de prueba: {len(self.logica.dar_entrenamientos(persona.id))}')

        reporte = self.logica.dar_reporte(persona1.id)
        entrenamientos = reporte["estadisticas"]["entrenamientos"]

        # Verificaciones
        self.assertEqual(len(entrenamientos), 1, "Debe haber una única fecha agrupada")

    def test_suma_repeticiones_por_fecha(self):
        # Caso 5: Se suman correctamente las repeticiones por fecha que hay al menos un entrenamiento
        persona1 = Persona(nombre=self.data_factory.unique.name(),
                           apellidos=self.data_factory.unique.name(),
                           talla=self.data_factory.random.uniform(0.0, 3.5),
                           peso=self.data_factory.random_int(0, 300),
                           edad=self.data_factory.random_int(0, 300),
                           brazo=self.data_factory.random_int(0, 300),
                           cintura=self.data_factory.random_int(0, 300),
                           pierna=self.data_factory.random_int(0, 300))
        self.session.add(persona1)
        self.session.commit()
        print(f'\n--Caso 5--')
        print(f'\n--Nueva Persona--')
        print(f'Persona creada: {persona1.id} - {persona1.nombre}')

        ejercicio1 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://youtube.com/watch?v=test1",
            calorias=self.data_factory.random_int(5, 50)
        )
        self.session.add(ejercicio1)
        self.session.commit()
        print(f'\n--Nuevo Ejercicio--')
        print(f'Ejercicio creado: {ejercicio1.id} - {ejercicio1.nombre}')

        fecha1 = datetime.now().date().strftime("%Y-%m-%d")
        entrenamiento1 = {
            "persona": persona1,
            "ejercicio": ejercicio1.nombre,
            "fecha": fecha1,
            "repeticiones": 13,
            "tiempo": str(time(0, 5, 30))
        }
        validacion1 = self.logica.validar_crear_editar_entrenamiento(**entrenamiento1)
        print(validacion1)
        resultado1 = self.logica.crear_entrenamiento(**entrenamiento1)
        print(f'\nResultado: {resultado1}')

        entrenamiento2 = {
            "persona": persona1,
            "ejercicio": ejercicio1.nombre,
            "fecha": fecha1,
            "repeticiones": 17,
            "tiempo": str(time(0, 5, 30))
        }
        validacion2 = self.logica.validar_crear_editar_entrenamiento(**entrenamiento2)
        print(validacion2)
        resultado2 = self.logica.crear_entrenamiento(**entrenamiento2)
        print(f'\nResultado: {resultado2}')

        reporte = self.logica.dar_reporte(persona1.id)
        print(f"\nReporte obtenido: {reporte}")
        self.assertEqual(reporte["estadisticas"]["total_repeticiones"], 30,
                         "La suma de las repeticiones por día no es correcta")

    def test_suma_calorias_por_fecha(self):
        # Caso 6: Se suman correctamente las calorías por fecha
        persona1 = Persona(nombre=self.data_factory.unique.name(),
                           apellidos=self.data_factory.unique.name(),
                           talla=self.data_factory.random.uniform(0.0, 3.5),
                           peso=self.data_factory.random_int(0, 300),
                           edad=self.data_factory.random_int(0, 300),
                           brazo=self.data_factory.random_int(0, 300),
                           cintura=self.data_factory.random_int(0, 300),
                           pierna=self.data_factory.random_int(0, 300))
        self.session.add(persona1)
        self.session.commit()

        print(f'\n--Caso 6--')
        print(f'\n--Nueva Persona--')
        print(f'\nPersona creada: {persona1.id} - {persona1.nombre}')

        ejercicio1 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://youtube.com/watch?v=test1",
            calorias=10
        )
        self.session.add(ejercicio1)
        self.session.commit()
        print(f'\n--Nuevo Ejercicio--')
        print(f'\nEjercicio creado: {ejercicio1.id} - {ejercicio1.nombre}')

        ejercicio2 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://youtube.com/watch?v=test1",
            calorias=5
        )
        self.session.add(ejercicio2)
        self.session.commit()
        print(f'\n--Nuevo Ejercicio--')
        print(f'\nEjercicio creado: {ejercicio2.id} - {ejercicio2.nombre}')

        fecha1 = datetime.now().date().strftime("%Y-%m-%d")
        entrenamiento1 = {
            "persona": persona1,
            "ejercicio": ejercicio1.nombre,
            "fecha": fecha1,
            "repeticiones": 10,
            "tiempo": str(time(0, 5, 30))
        }
        validacion1 = self.logica.validar_crear_editar_entrenamiento(**entrenamiento1)
        print(validacion1)
        resultado1 = self.logica.crear_entrenamiento(**entrenamiento1)
        print(f'\nResultado: {resultado1}')

        entrenamiento2 = {
            "persona": persona1,
            "ejercicio": ejercicio2.nombre,
            "fecha": fecha1,
            "repeticiones": 30,
            "tiempo": str(time(0, 5, 30))
        }
        validacion2 = self.logica.validar_crear_editar_entrenamiento(**entrenamiento2)
        print(validacion2)
        resultado2 = self.logica.crear_entrenamiento(**entrenamiento2)
        print(f'\nResultado: {resultado2}')

        reporte = self.logica.dar_reporte(persona1.id)
        print(f"\nReporte obtenido: {reporte}")
        self.assertEqual(reporte["estadisticas"]["total_calorias"], 250, "La suma de las calorías por día no es correcta")

    def test_reporte_orden_descendente(self):
        # Caso 7: El reporte se presenta ordenado de más reciente a más antiguo
        persona1 = Persona(nombre=self.data_factory.unique.name(),
                           apellidos=self.data_factory.unique.name(),
                           talla=self.data_factory.random.uniform(0.0, 3.5),
                           peso=self.data_factory.random_int(0, 300),
                           edad=self.data_factory.random_int(0, 300),
                           brazo=self.data_factory.random_int(0, 300),
                           cintura=self.data_factory.random_int(0, 300),
                           pierna=self.data_factory.random_int(0, 300))
        self.session.add(persona1)
        self.session.commit()

        print(f'\n--Caso 6--')
        print(f'\n--Nueva Persona--')
        print(f'\nPersona creada: {persona1.id} - {persona1.nombre}')

        ejercicio1 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://youtube.com/watch?v=test1",
            calorias=10
        )
        self.session.add(ejercicio1)
        self.session.commit()
        print(f'\n--Nuevo Ejercicio--')
        print(f'\nEjercicio creado: {ejercicio1.id} - {ejercicio1.nombre}')

        ejercicio2 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://youtube.com/watch?v=test1",
            calorias=5
        )
        self.session.add(ejercicio2)
        self.session.commit()
        print(f'\n--Nuevo Ejercicio--')
        print(f'\nEjercicio creado: {ejercicio2.id} - {ejercicio2.nombre}')

        fecha1 = "2024-03-02"
        fecha2 = "2025-03-02"
        entrenamiento1 = {
            "persona": persona1,
            "ejercicio": ejercicio1.nombre,
            "fecha": fecha2,
            "repeticiones": self.data_factory.random_int(0, 300),
            "tiempo": str(time(0, 5, 30))
        }
        validacion1 = self.logica.validar_crear_editar_entrenamiento(**entrenamiento1)
        print(validacion1)
        resultado1 = self.logica.crear_entrenamiento(**entrenamiento1)
        print(f'\nResultado: {resultado1}')

        entrenamiento2 = {
            "persona": persona1,
            "ejercicio": ejercicio2.nombre,
            "fecha": fecha1,
            "repeticiones": self.data_factory.random_int(0, 300),
            "tiempo": str(time(0, 5, 30))
        }
        validacion2 = self.logica.validar_crear_editar_entrenamiento(**entrenamiento2)
        print(validacion2)
        resultado2 = self.logica.crear_entrenamiento(**entrenamiento2)
        print(f'\nResultado: {resultado2}')

        reporte = self.logica.dar_reporte(persona1.id)
        print(f"\nReporte obtenido: {reporte}")

        entrenamientos = reporte["estadisticas"]["entrenamientos"]
        self.assertEqual(entrenamientos[0]["fecha"], fecha2,
                         "El entrenamiento más reciente no se encuentra en primer lugar en el reporte")

    def test_totales_historicos_repeticiones_calorias(self):
        #Caso 8: Se muestra el total de repeticiones o ejercicos y de calorías en la última fila del reporte

        persona1 = Persona(nombre=self.data_factory.unique.name(),
                           apellidos=self.data_factory.unique.name(),
                           talla=self.data_factory.random.uniform(0.0, 3.5),
                           peso=self.data_factory.random_int(0, 300),
                           edad=self.data_factory.random_int(0, 300),
                           brazo=self.data_factory.random_int(0, 300),
                           cintura=self.data_factory.random_int(0, 300),
                           pierna=self.data_factory.random_int(0, 300))
        self.session.add(persona1)
        self.session.commit()

        print(f'\n--Caso 6--')
        print(f'\n--Nueva Persona--')
        print(f'\nPersona creada: {persona1.id} - {persona1.nombre}')

        ejercicio1 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://youtube.com/watch?v=test1",
            calorias=10
        )
        self.session.add(ejercicio1)
        self.session.commit()
        print(f'\n--Nuevo Ejercicio--')
        print(f'\nEjercicio creado: {ejercicio1.id} - {ejercicio1.nombre}')

        ejercicio2 = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://youtube.com/watch?v=test1",
            calorias=5
        )
        self.session.add(ejercicio2)
        self.session.commit()
        print(f'\n--Nuevo Ejercicio--')
        print(f'\nEjercicio creado: {ejercicio2.id} - {ejercicio2.nombre}')

        fecha1 = "2024-03-02"
        fecha2 = "2025-03-02"
        entrenamiento1 = {
            "persona": persona1,
            "ejercicio": ejercicio1.nombre,
            "fecha": fecha2,
            "repeticiones": 15,
            "tiempo": str(time(0, 5, 30))
        }
        validacion1 = self.logica.validar_crear_editar_entrenamiento(**entrenamiento1)
        print(validacion1)
        resultado1 = self.logica.crear_entrenamiento(**entrenamiento1)
        print(f'\nResultado: {resultado1}')

        entrenamiento2 = {
            "persona": persona1,
            "ejercicio": ejercicio2.nombre,
            "fecha": fecha1,
            "repeticiones": 10,
            "tiempo": str(time(0, 5, 30))
        }
        validacion2 = self.logica.validar_crear_editar_entrenamiento(**entrenamiento2)
        print(validacion2)
        resultado2 = self.logica.crear_entrenamiento(**entrenamiento2)
        print(f'\nResultado: {resultado2}')

        reporte = self.logica.dar_reporte(persona1.id)
        print(f"\nReporte obtenido: {reporte}")

        entrenamientos = reporte["estadisticas"]["entrenamientos"]

        self.assertEqual(reporte["estadisticas"]["total_calorias"], 200, "El total de calorías en el reporte no es corrwecto")
        self.assertEqual(reporte["estadisticas"]["total_repeticiones"], 25, "El total de calorías en el reporte no es corrwecto")