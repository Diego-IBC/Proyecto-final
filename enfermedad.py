class Enfermedad:
    def __init__(self, nombre, prob_infeccion_familia, prob_infeccion_conocido, prom_pasos):
        self.nombre = nombre
        self.prob_infeccion_familia = prob_infeccion_familia
        self.prob_infeccion_conocido = prob_infeccion_conocido
        self.prom_pasos = prom_pasos
