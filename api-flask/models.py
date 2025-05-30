from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    parametro = db.Column(db.String(100))
    fecha_hora = db.Column(db.DateTime, nullable=False)
    ip_usuario = db.Column(db.String(100), nullable=False)
