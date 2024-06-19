import csv
from collections import defaultdict # nueva libreria
import unittest # Pruebas unitarias
# el programa deberá calcular el ganador de votos validos considerando que los siguientes datos son proporcionados:
# region,provincia,distrito,dni,candidato,esvalido
# Si hay un candidato con >50% de votos válidos retornar un array con un string con el nombre del ganador
# Si no hay un candidato que cumpla la condicion anterior, retornar un array con los dos candidatos que pasan a segunda vuelta
# Si ambos empatan con 50% de los votos se retorna el que apareció primero en el archivo
# el DNI debe ser valido (8 digitos)
class CalculaGanador:

    def leerdatos(self):
        #  Lee los datos del archivo CSV especificado y 
        # retorna una lista de listas con los datos.
        data = []
        with open('0204.csv', 'r') as csvfile:
            next(csvfile)  # Salta la primera linea de encabezado
            datareader = csv.reader(csvfile)
            for fila in datareader:
                data.append( fila)
        return data

    def calcularganador(self, data):
        # Calcula el ganador de los votos válidos según las reglas especificadas.
        # Retorna una lista con el nombre del ganador o 
        # los dos candidatos que pasan a segunda vuelta
        
        # Uso de defaultdict para inicializar los contadores de votos de manera más eficiente
        votosxcandidato = defaultdict(int)
        total_votos_validos = 0 # acumulador de votos válidos

        #  
        for fila in data:
            dni, candidato, esvalido = fila[3], fila[4], fila[5]
            # Verificación de que el DNI sea válido y el voto sea válido
            if len(dni) == 8 and esvalido == '1':
                votosxcandidato[candidato] += 1
                total_votos_validos += 1
                
        # Ordenar candidatos por cantidad de votos válidos en orden descendente
        # Lista de tuplas de tipo "(nombre_candidato, votos_candidatos)"
        # Técnica: Simplificación de condicionales y eliminación de código duplicado
        ordenado = sorted(votosxcandidato.items(), key=lambda item: item[1], reverse=True)

        # Evaluar si algún candidato tiene más del 50% de los votos válidos
        # Técnica: Simplificación de condicionales
        ganador_potencial, votos_ganador_potencial = ordenado[0]
        if votos_ganador_potencial > (total_votos_validos / 2):
            return [ganador_potencial]
        
        # Evaluar si hay empate en el primer lugar con exactamente el 50% de los votos
        segundo_potencial, votos_segundo_potencial = ordenado[1]
        if votos_ganador_potencial == votos_segundo_potencial == (total_votos_validos / 2):
            return [ganador_potencial]

        return [ganador_potencial, segundo_potencial]

class TestCalculaGanador(unittest.TestCase):

    def setUp(self):
        self.calculadora = CalculaGanador()

    def test_un_candidato_gana(self):
        datos = [
            ['Áncash', 'Asunción', 'Acochaca', '40810062', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '50533597', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '80777322', 'Aundrea Grace', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '13017965', 'Aundrea Grace', '0'],
        ]
        resultado_esperado = ['Eddie Hinesley']
        resultado_obtenido = self.calculadora.calcularganador(datos)
        self.assertEqual(resultado_obtenido, resultado_esperado)

    def test_empate_f1(self):
        datos = [
            ['Áncash', 'Asunción', 'Acochaca', '40810062', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '50533597', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '80777322', 'Aundrea Grace', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '13017965', 'Aundrea Grace', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '13717965', 'Nuevo Candidato', '0']
        ]
        resultado_esperado = ['Eddie Hinesley']
        resultado_obtenido = self.calculadora.calcularganador(datos)
        self.assertEqual(resultado_obtenido, resultado_esperado)

    def test_empate_f2(self):
        datos = [
            ['Áncash', 'Asunción', 'Acochaca', '40810062', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '50533597', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '80777322', 'Aundrea Grace', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '13017965', 'Aundrea Grace', '1']
        ]
        resultado_esperado = ['Eddie Hinesley']
        resultado_obtenido = self.calculadora.calcularganador(datos)
        self.assertEqual(resultado_obtenido, resultado_esperado)

if __name__ == '__main__':
    unittest.main()
