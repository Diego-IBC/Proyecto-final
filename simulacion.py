import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Simulacion:
    def __init__(self, enfermedad, todas_las_personas):
        self.enfermedad = enfermedad
        self.todas_las_personas = todas_las_personas
        self.primer_infectado = None
        self.resultados_simulacion = {'S': [], 'I': [], 'R': []}

    def simular_sir(self, dias):
        beta_familia = self.enfermedad.prob_infeccion_familia
        beta_conocido = self.enfermedad.prob_infeccion_conocido
        gamma = 1 / self.enfermedad.prom_pasos

        susceptibles = [persona for persona in self.todas_las_personas if persona.estado == 'susceptible']
        infectados = [persona for persona in self.todas_las_personas if persona.estado == 'infectado']
        recuperados = [persona for persona in self.todas_las_personas if persona.estado == 'Recuperado']

        if susceptibles:
            primer_infectado = np.random.choice(susceptibles)
            primer_infectado.infectar()
            infectados.append(primer_infectado)
            susceptibles.remove(primer_infectado)
            self.primer_infectado = primer_infectado

        S_arr = np.zeros(dias + 1)
        I_arr = np.zeros(dias + 1)
        R_arr = np.zeros(dias + 1)

        S_arr[0] = len(susceptibles)
        I_arr[0] = len(infectados)
        R_arr[0] = len(recuperados)

        for t in range(dias):
            nuevos_infectados = []
            nuevos_recuperados = []

            for persona_infectada in infectados[:]:
                for conocido in persona_infectada.conocidos:
                    if conocido.estado == 'susceptible' and conocido not in nuevos_infectados:
                        if persona_infectada.familia == conocido.familia:
                            prob_infeccion = beta_familia
                        else:
                            prob_infeccion = beta_conocido
                        
                        if np.random.rand() < prob_infeccion:
                            conocido.infectar(persona_infectada)
                            nuevos_infectados.append(conocido)
                            susceptibles.remove(conocido) 

            for persona_infectada in infectados[:]:
                if np.random.rand() < gamma:
                    persona_infectada.recuperar()
                    nuevos_recuperados.append(persona_infectada)

            infectados.extend(nuevos_infectados)
            for recuperado in nuevos_recuperados:
                infectados.remove(recuperado)
                recuperados.append(recuperado)

            S_arr[t + 1] = len(susceptibles)
            I_arr[t + 1] = len(infectados)
            R_arr[t + 1] = len(recuperados)

            
            self.resultados_simulacion['S'].append(S_arr[t + 1])
            self.resultados_simulacion['I'].append(I_arr[t + 1])
            self.resultados_simulacion['R'].append(R_arr[t + 1])

            print("--------------------------------------------------------------")
            print(f"Día {t + 1}: Total de susceptibles: {int(S_arr[t + 1])}, Total de infectados: {int(I_arr[t + 1])}, Total de recuperados: {int(R_arr[t + 1])}")

       
        self.guardar_resultados_csv()

        
        archivo_imagen = self.plot_resultados(S_arr, I_arr, R_arr, dias)
        self.mostrar_primer_infectado()

    def guardar_resultados_csv(self, archivo='resultados_simulacion.csv'):
        data = {
            'Dia': range(len(self.resultados_simulacion['S'])),
            'Susceptibles': self.resultados_simulacion['S'],
            'Infectados': self.resultados_simulacion['I'],
            'Recuperados': self.resultados_simulacion['R']
        }
        df = pd.DataFrame(data)
        df.to_csv(archivo, index=False)

    def plot_resultados(self, S, I, R, dias):
        tiempo = np.arange(dias + 1)
        fig, ax = plt.subplots()
        ax.plot(tiempo, S, label='Susceptibles')
        ax.plot(tiempo, I, label='Infectados')
        ax.plot(tiempo, R, label='Recuperados')
        ax.set_title('Modelo SIR: Susceptibles, Infectados, Recuperados')
        ax.set_xlabel('Días')
        ax.set_ylabel('Número de Individuos')
        ax.legend()
        ax.grid(True)

        fig.tight_layout()

        
        archivo_imagen = 'grafico_simulacion.png'
        fig.savefig(archivo_imagen)
        plt.close(fig) 

        return archivo_imagen

    def mostrar_primer_infectado(self):
        if self.primer_infectado:
            print(f"El primer infectado fue {self.primer_infectado.nombre_apellido}.")
        else:
            print("No hay información sobre el primer infectado.")
