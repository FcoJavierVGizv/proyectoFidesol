from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
from models import db, Consulta
from collections import Counter
import requests

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/paises', methods=['GET'])
def buscar_paises():
    nombre = request.args.get('nombre')
    if not nombre:
        return jsonify({'error': 'Falta parámetro nombre'}), 400

    url_api = f"https://restcountries.com/v3.1/name/{nombre}"
    respuesta = requests.get(url_api)

    if respuesta.status_code != 200:
        return jsonify({'error': 'Error consultando API externa'}), 502

    data_paises = respuesta.json()

    nueva_consulta = Consulta(
        tipo='pais',
        parametro=nombre,
        fecha_hora=datetime.now(),
        ip_usuario=request.remote_addr
    )
    db.session.add(nueva_consulta)
    db.session.commit()

    return jsonify(data_paises)


@app.route('/consultas', methods=['GET'])
def obtener_consultas():
    consultas = Consulta.query.order_by(Consulta.fecha_hora.desc()).all()
    resultado = [{
        'tipo': c.tipo,
        'parametro': c.parametro,
        'fecha_hora': c.fecha_hora.isoformat(),
        'ip_usuario': c.ip_usuario
    } for c in consultas]
    return jsonify(resultado)


@app.route('/estadisticas', methods=['GET'])
def estadisticas():
    consultas = Consulta.query.all()
    total_por_tipo = Counter([c.tipo for c in consultas])
    parametros = [c.parametro for c in consultas if c.parametro]
    mas_consultado = Counter(parametros).most_common(1)
    por_dia = Counter([c.fecha_hora.date().isoformat() for c in consultas])
    return jsonify({
        'total_por_tipo': dict(total_por_tipo),
        'mas_consultado': mas_consultado[0] if mas_consultado else None,
        'consultas_por_dia': dict(por_dia)
    })


@app.route('/')
def inicio():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
