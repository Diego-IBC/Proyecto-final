import csv
import random

nombres = [
    "Alejandro", "Sofía", "Juan", "Valentina", "Carlos", "Camila", "Manuel", "Isabella", "José", "Emma",
    "Javier", "Lucía", "Diego", "Martina", "Pablo", "Victoria", "Luis", "Paula", "Fernando", "María",
    "Antonio", "Laura", "Miguel", "Daniela", "Sergio", "Andrea", "Eduardo", "Natalia", "Mario", "Elena",
    "Francisco", "Sara", "Daniel", "Valeria", "Guillermo", "Adriana", "Jorge", "Gabriela", "Ignacio", "Clara",
    "Ricardo", "Julia", "Mateo", "Alba", "Gonzalo", "Carmen", "Rubén", "Rosa", "Víctor", "Lorena",
    "Rafael", "Patricia", "Álvaro", "Marina", "Andrés", "Beatriz", "Ramón", "Ana", "Germán", "Silvia",
    "Arturo", "Aitana", "Javier", "Ainhoa", "Iván", "Noelia", "Raúl", "Isabel", "Hugo", "Elena",
    "Óscar", "Marta", "Samuel", "Inés", "Tomás", "Sara", "Rodrigo", "Iris", "Martín", "Adriana",
    "Emilio", "Elena", "Israel", "Elisa", "Alonso", "Ángela", "Enrique", "Claudia", "Lucas", "Lorena",
    "Nicolás", "Diana", "Miguel Ángel", "Patricia", "Adrián", "Raquel", "Alejandro", "Olga", "Francisco Javier", "Carmen"
]
apellidos = [
    "García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Martín",
    "Jiménez", "Ruiz", "Hernández", "Díaz", "Moreno", "Álvarez", "Muñoz", "Romero", "Alonso", "Gutiérrez",
    "Navarro", "Torres", "Domínguez", "Vázquez", "Ramos", "Gil", "Ramírez", "Serrano", "Blanco", "Molina",
    "Morales", "Ortega", "Delgado", "Castro", "Ortiz", "Rubio", "Marín", "Sanz", "Iglesias", "Núñez",
    "Medina", "Garrido", "Cortés", "Castillo", "Suárez", "Peña", "Vidal", "Fuentes", "Cabrera", "Reyes",
    "Calvo", "Arias", "Cruz", "Pascual", "Gallardo", "Herrero", "Flores", "Diez", "Lorenzo", "Herrera",
    "Montero", "Aguilar", "Santos", "Giménez", "Ibáñez", "Vega", "León", "Méndez", "Campos", "Caballero",
    "Cano", "Luque", "Carmona", "Valero", "Santiago", "Pardo", "Esteban", "Bravo", "Guerrero", "Rojas",
    "Montoya", "Moya", "Soler", "Parra", "Vila", "Olivares", "Redondo", "Aguilera", "Soto", "Perea"
]


nombres_aleatorios = random.choices(nombres, k=1000)
apellidos_aleatorios = random.choices(apellidos, k=1000)


ids_aleatorios = random.sample(range(1, 1001), 1000)

ciudadanos = []
for i in range(1000):
    nombre_apellido = f"{nombres_aleatorios[i]} {apellidos_aleatorios[i]}"
    id_aleatorio = ids_aleatorios[i]
    familia = apellidos_aleatorios[i]
    estado = "susceptible"  
    ciudadanos.append([nombre_apellido, id_aleatorio, familia, estado])

with open("ciudadanos.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["nombre_apellido", "id", "familia", "estado"]) 
    writer.writerows(ciudadanos)

print("Archivo CSV generado con éxito.")
