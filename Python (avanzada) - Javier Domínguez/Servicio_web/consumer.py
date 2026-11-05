import json
import requests

url = 'http://localhost:9000/alumnos'

try:
    response = requests.get(url)

    print(f'Respuesta obtenida en {response.elapsed.total_seconds()} segundos.')

    response_dict = json.loads(response.text)

    for alumno in response_dict['alumnos']:
        print(f'{alumno["nombre"]} {alumno["apellidos"]}')

except Exception as err:
    print(f'Ha habido un error: {err}')