import numpy as np

class Comunidad:
    def __init__(self, nombre, personas):
        self.nombre = nombre
        self.personas = personas

    def num_ciudadanos(self):
        return len(self.personas)

    def generar_comunidades(personas, max_comunidades=1000, max_personas_por_comunidad=None):
        comunidades = []
        count = 0
        familias = {}

        for persona in personas:
            if persona.familia not in familias:
                familias[persona.familia] = []
            familias[persona.familia].append(persona)

        for familia, miembros in familias.items():
            comunidad = Comunidad(nombre=f"Comunidad {len(comunidades) + 1}", personas=miembros)
            comunidades.append(comunidad)
            count += 1
            if count >= max_comunidades:
                break

        return comunidades


    def conectar_personas(personas, max_conocidos = None):
        for persona in personas:
            num_conocidos = np.random.randint(1, max_conocidos + 1)
            persona.conocidos = list(np.random.choice(personas, num_conocidos, replace=False))