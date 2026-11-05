import json

from werkzeug.wrappers import Response
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hola mundo!</h1>'

@app.route('/alumnos')
def get_alumnos():
    data = {
        'centro': 'Universidad Complutense de Madrid',
        'alumnos': [
            {'id': '00', 'matrícula': '1234QSPM', 'nombre': 'Mari Carmen', 'apellidos': 'García', 'clase': 'A'},
            {'id': '01', 'matrícula': '1234NDFK', 'nombre': 'Antonio', 'apellidos': 'Rodríguez', 'clase': 'A'},
            {'id': '02', 'matrícula': '1234KWSH', 'nombre': 'María', 'apellidos': 'González', 'clase': 'B'},
            {'id': '03', 'matrícula': '1234ZMLD', 'nombre': 'Manuel', 'apellidos': 'Fernández', 'clase': 'A'},
            {'id': '04', 'matrícula': '1234POWM', 'nombre': 'Carmen', 'apellidos': 'López', 'clase': 'A'},
            {'id': '05', 'matrícula': '1234LJBF', 'nombre': 'Jose', 'apellidos': 'Martínez', 'clase': 'B'},
            {'id': '06', 'matrícula': '1234GQKD', 'nombre': 'Ana María', 'apellidos': 'Sánchez', 'clase': 'B'},
            {'id': '07', 'matrícula': '1234KJEM', 'nombre': 'Francisco', 'apellidos': 'Pérez', 'clase': 'A'},
            {'id': '08', 'matrícula': '1234TTMK', 'nombre': 'María Pilar', 'apellidos': 'Gómez', 'clase': 'A'},
            {'id': '09', 'matrícula': '1234EFRW', 'nombre': 'David', 'apellidos': 'Martín', 'clase': 'A'},
            {'id': '10', 'matrícula': '1234LWJB', 'nombre': 'Laura', 'apellidos': 'Jiménez', 'clase': 'B'},
            {'id': '11', 'matrícula': '1234GFDV', 'nombre': 'Juan', 'apellidos': 'Hernández', 'clase': 'B'},
            {'id': '12', 'matrícula': '1234MKWX', 'nombre': 'Josefa', 'apellidos': 'Ruíz', 'clase': 'B'},
            {'id': '13', 'matrícula': '1234NSHC', 'nombre': 'Javier', 'apellidos': 'Díaz', 'clase': 'A'},
            {'id': '14', 'matrícula': '1234PCER', 'nombre': 'Isabel', 'apellidos': 'Moreno', 'clase': 'B'},
            {'id': '15', 'matrícula': '1234AHIV', 'nombre': 'Jose Antonio', 'apellidos': 'Muñoz', 'clase': 'A'},
            {'id': '16', 'matrícula': '1234MCTM', 'nombre': 'María Dolores', 'apellidos': 'Álvarez','clase': 'B'}
        ]
    }
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json'
    )

if __name__ == '__main__':
    from werkzeug.serving import run_simple

    run_simple('localhost', 9000, app)
