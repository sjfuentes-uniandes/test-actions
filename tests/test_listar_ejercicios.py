import unittest
from faker import Faker
from src.modelo.ejercicio import Ejercicio
from src.logica.logicaEnForma import LogicaEnForma
from src.modelo.declarative_base import Session, Base, engine
from src.modelo.entrenamiento import Entrenamiento

class Test_Listar_Ejercicios(unittest.TestCase):
    def setUp(self):
        self.logica = LogicaEnForma()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.data_factory = Faker()
        Faker.seed(1000)

    def tearDown(self):
        self.session = Session()
        busqueda = self.session.query(Ejercicio).all()
        for entrenamiento in busqueda:
            self.session.delete(entrenamiento)
        self.session.commit()
        self.session.close()

    def test_no_hay_ejercicios(self):
        #Caso 1: No hay ejercicios creados para mostrar
        lista_ejercicios = self.logica.dar_ejercicios()
        self.assertEqual(len(lista_ejercicios), 0, "No hay ejercicios")

    def test_lista_ejercicio(self):
        #Caso 2: Existe un ejercicio y lo muestra en la lista
        ejercicio_prueba = Ejercicio(
            nombre=self.data_factory.word(),
            descripcion=self.data_factory.sentence(),
            enlace="https://youtu.be/" + self.data_factory.word(),
            calorias=self.data_factory.random_int(5, 50)
        )
        self.session.add(ejercicio_prueba)
        self.session.commit()
        lista_ejercicio = self.logica.dar_ejercicios()
        self.assertIsInstance(lista_ejercicio, list, "No trae una lista de ejercicio")
        self.assertEqual(len(lista_ejercicio), 1, "No hay ejercicios")

    def test_lista_diccionarios_ejercicios(self):
        # Caso 3: Se listan ejercicios cuando se envía una lista de ejercicios como diccionario según lo espera vista
        self.session.query(Ejercicio).delete()
        self.session.commit()

        ejercicio_prueba_1 = Ejercicio(nombre=self.data_factory.word(), descripcion=self.data_factory.sentence(),
                                       enlace="https://youtu.be/" + self.data_factory.word(),
                                       calorias=self.data_factory.random_int(5, 50))
        self.session.add(ejercicio_prueba_1)
        ejercicio_prueba_2 = Ejercicio(nombre=self.data_factory.word(), descripcion=self.data_factory.sentence(),
                                       enlace="https://youtu.be/" + self.data_factory.word(),
                                       calorias=self.data_factory.random_int(5, 50))
        self.session.add(ejercicio_prueba_2)
        ejercicio_prueba_3 = Ejercicio(nombre=self.data_factory.word(), descripcion=self.data_factory.sentence(),
                                       enlace="https://youtu.be/" + self.data_factory.word(),
                                       calorias=self.data_factory.random_int(5, 50))
        self.session.add(ejercicio_prueba_3)
        ejercicio_prueba_4 = Ejercicio(nombre=self.data_factory.word(), descripcion=self.data_factory.sentence(),
                                       enlace="https://youtu.be/" + self.data_factory.word(),
                                       calorias=self.data_factory.random_int(5, 50))
        self.session.add(ejercicio_prueba_4)
        ejercicio_prueba_5 = Ejercicio(nombre=self.data_factory.word(), descripcion=self.data_factory.sentence(),
                                       enlace="https://youtu.be/" + self.data_factory.word(),
                                       calorias=self.data_factory.random_int(5, 50))
        self.session.add(ejercicio_prueba_5)
        ejercicio_prueba_6 = Ejercicio(nombre=self.data_factory.word(), descripcion=self.data_factory.sentence(),
                                       enlace="https://youtu.be/" + self.data_factory.word(),
                                       calorias=self.data_factory.random_int(5, 50))
        self.session.add(ejercicio_prueba_6)
        self.session.commit()

        lista_ejercicios = self.logica.dar_ejercicios(como_diccionario=True)

        self.assertIsInstance(lista_ejercicios[0], dict, "Los elementos de la lista no son diccionarios")
        keys_ejercicios = {"nombre", "descripcion", "enlace", "calorias"}
        self.assertTrue(keys_ejercicios.issubset(lista_ejercicios[0].keys()),
                        "Los elementos de la lista no son Ejercicios")

    def test_lista_ejercicios_orden_alfabeticos(self):
        #Caso 4: Los ejercicios están ordenados alfabeticamente

        self.session.query(Ejercicio).delete()
        self.session.commit()

        ejercicio_prueba_1 = Ejercicio(nombre="c", descripcion=self.data_factory.sentence(),
                                       enlace="https://youtu.be/" + self.data_factory.word(),
                                       calorias=self.data_factory.random_int(5, 50))
        self.session.add(ejercicio_prueba_1)
        ejercicio_prueba_2 = Ejercicio(nombre="Z", descripcion=self.data_factory.sentence(),
                                       enlace="https://youtu.be/" + self.data_factory.word(),
                                       calorias=self.data_factory.random_int(5, 50))
        self.session.add(ejercicio_prueba_2)
        ejercicio_prueba_3 = Ejercicio(nombre="a", descripcion=self.data_factory.sentence(),
                                       enlace="https://youtu.be/" + self.data_factory.word(),
                                       calorias=self.data_factory.random_int(5, 50))
        self.session.add(ejercicio_prueba_3)
        ejercicio_prueba_4 = Ejercicio(nombre="n", descripcion=self.data_factory.sentence(),
                                       enlace="https://youtu.be/" + self.data_factory.word(),
                                       calorias=self.data_factory.random_int(5, 50))
        self.session.add(ejercicio_prueba_4)
        ejercicio_prueba_5 = Ejercicio(nombre="m", descripcion=self.data_factory.sentence(),
                                       enlace="https://youtu.be/" + self.data_factory.word(),
                                       calorias=self.data_factory.random_int(5, 50))
        self.session.add(ejercicio_prueba_5)
        ejercicio_prueba_6 = Ejercicio(nombre="H", descripcion=self.data_factory.sentence(),
                                       enlace="https://youtu.be/" + self.data_factory.word(),
                                       calorias=self.data_factory.random_int(5, 50))
        self.session.add(ejercicio_prueba_6)
        self.session.commit()

        lista_ejercicios = self.logica.dar_ejercicios()

        self.assertEqual(lista_ejercicios[0].nombre, "a", "El primer ejercicio debería ser a")
        self.assertEqual(lista_ejercicios[5].nombre, "Z", "El último ejercicio debería ser Z")
