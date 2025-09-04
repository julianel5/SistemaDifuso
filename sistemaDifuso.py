import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definir la variable de entrada (velocidad del coche)
velocidad = ctrl.Antecedent(np.arange(0, 121, 1), 'velocidad')  # 0 a 120 km/h

# Definir la variable de salida (nivel de velocidad percibida)
nivel = ctrl.Consequent(np.arange(0, 11, 1), 'nivel')

# Definir conjuntos difusos para la entrada (velocidad)
velocidad['baja'] = fuzz.trimf(velocidad.universe, [0, 0, 60])
velocidad['media'] = fuzz.trimf(velocidad.universe, [40, 60, 100])
velocidad['alta'] = fuzz.trimf(velocidad.universe, [80, 120, 120])

# Definir conjuntos difusos para la salida (nivel percibido de velocidad)
nivel['baja'] = fuzz.trimf(nivel.universe, [0, 0, 5])
nivel['media'] = fuzz.trimf(nivel.universe, [2, 5, 8])
nivel['alta'] = fuzz.trimf(nivel.universe, [6, 10, 10])

# Definir reglas difusas
regla1 = ctrl.Rule(velocidad['baja'], nivel['baja'])
regla2 = ctrl.Rule(velocidad['media'], nivel['media'])
regla3 = ctrl.Rule(velocidad['alta'], nivel['alta'])
regla4 = ctrl.Rule(velocidad['baja'] & velocidad['media'], nivel['media'])
regla5 = ctrl.Rule(velocidad['media'] & velocidad['alta'], nivel['alta'])

# Crear el sistema de control
sistema_ctrl = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5])
sistema = ctrl.ControlSystemSimulation(sistema_ctrl)

# Pedir datos al usuario
vel_input = float(input("Ingrese la velocidad del coche en km/h: "))
sistema.input['velocidad'] = vel_input

# Computar resultado
sistema.compute()

print(f"\nLa velocidad ingresada es {vel_input} km/h")
print(f"Clasificación difusa: {sistema.output['nivel']:.2f} (0=baja, 10=alta)")

# Mostrar resultado gráfico
nivel.view(sim=sistema)
velocidad.view(sim=sistema)
