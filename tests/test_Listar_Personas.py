import unittest
from faker import Faker
from src.modelo.persona import Persona
from src.logica.logicaEnForma import LogicaEnForma
from src.modelo.declarative_base import Session, Base, engine

class Test_ListarPersonas(unittest.TestCase):
    def setUp(self):
        self.logica = LogicaEnForma()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.fake = Faker()

    def tearDown(self):
        self.session = Session()
        busqueda = self.session.query(Persona).all()
        for persona in busqueda:
            self.session.delete(persona)
        self.session.commit()
        self.session.close()


    def test_listar_personas_lista_vacia(self):
        #Caso 1: Retorna lista vacía si no hay personas registradas en En Forma
        personas = self.logica.dar_personas()
        self.assertIsInstance(personas, list, "El resultado no es una lista")
        self.assertEqual(len(personas), 0, "La lista está vacía")

    def test_listar_personas_tipo_persona(self):
        #Caso 2: Verifica que dar_personas() retorne siempre una lista y que el contenido sea valido
        persona1 = Persona(nombre="Carlos", apellidos="Zapata", talla=1.70, peso=70, edad=25, brazo=30, cintura=80, pierna=40)
        self.session.add(persona1)
        self.session.commit()
        personas = self.logica.dar_personas()
        self.assertIsInstance(personas, list, "El resultado no es una lista")
        self.assertGreater(len(personas), 0, "Lista no debería estar vacía para esta prueba")
        for persona in personas:
            self.assertIsInstance(persona, Persona, "El resultado no es una instancia de Persona")

    def test_listar_personas_orden_alfabetico(self):
        #Caso 3: La lista de personas debe estar ordenada por nombre y luego por apellido en orden alfabético.
        persona1 = Persona(nombre="Carlos", apellidos="Zapata", talla=1.70, peso=70, edad=25, brazo=30, cintura=80, pierna=40)
        persona2 = Persona(nombre="Ana", apellidos="Martínez", talla=1.60, peso=60, edad=30, brazo=25, cintura=70, pierna=35)
        persona3 = Persona(nombre="Carlos", apellidos="Arango", talla=1.75, peso=75, edad=35, brazo=35, cintura=85, pierna=45)

        self.session.add(persona1)
        self.session.add(persona2)
        self.session.add(persona3)

        self.session.commit()
        
        consulta_ana = self.session.query(Persona).filter(Persona.nombre == "Ana").first()
        consulta_arango = self.session.query(Persona).filter(Persona.nombre == "Carlos", Persona.apellidos == "Arango").first()
        consulta_zapata = self.session.query(Persona).filter(Persona.nombre == "Carlos", Persona.apellidos == "Zapata").first()

        # Obtener lista desde la lógica
        lista_personas = self.logica.dar_personas()

        # Resultado esperado, usando los datos precargados
        esperado = [
            ("Ana", "Martínez"),
            ("Carlos", "Arango"),
            ("Carlos", "Zapata")
        ]

        self.assertEqual(
            [(persona.nombre, persona.apellidos) for persona in lista_personas],
            esperado,
            "La lista no está ordenada alfabéticamente por nombre y apellido"
        )

        self.session.delete(consulta_ana)
        self.session.delete(consulta_arango)
        self.session.delete(consulta_zapata)
        self.session.commit()

    def test_listar_personas_scroll(self):
        #Caso 4: Verifica que se habilite el scroll si hay muchas personas

        self.session.add_all([Persona(nombre=self.fake.first_name(), apellidos=self.fake.last_name()) for _ in range(100)])
        self.session.commit()

        lista_personas = self.logica.dar_personas()

        self.assertEqual(len(lista_personas), 100, "Se deben mostrar las 100 personas registradas")
        self.assertTrue(self.logica.scroll_habilitado(), "El scroll debería habilitarse al tener muchas personas que no caben en una sola vista de la pantalla")

        self.session.query(Persona).delete()
        self.session.commit()

    if __name__ == '__main__':
        unittest.main()
