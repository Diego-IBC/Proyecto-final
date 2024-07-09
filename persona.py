import pandas as pd

class Persona:
    def __init__(self, nombre_apellido, id, familia, estado='susceptible', enfermedad=None):
        self.nombre_apellido = nombre_apellido
        self.id = id
        self.familia = familia
        self.estado = estado
        self.enfermedad = enfermedad
        self.infectado_por = None
        self.conocidos = []

    def agregar_conocido(self, conocido):
        if conocido not in self.conocidos:
            self.conocidos.append(conocido)

    def infectar(self, infectado_por=None):
        if self.estado == 'susceptible':
            self.estado = 'infectado'
            self.infectado_por = infectado_por

    def recuperar(self):
        if self.estado == 'infectado':
            self.estado = 'Recuperado'

    @classmethod
    def leer_csv_y_crear_personas(cls, archivo_csv, enfermedad):
        personas = []
        df = pd.read_csv(archivo_csv)
        for index, row in df.iterrows():
            persona = cls(
                nombre_apellido=row['nombre_apellido'],
                id=row['id'],
                familia=row['familia'],
                estado=row.get('estado', 'susceptible'),
                enfermedad=enfermedad
            )
            personas.append(persona)

        return personas
