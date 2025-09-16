from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class TransportLine(db.Model):
    __tablename__ = 'transport_lines'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(20), nullable=False)  # 'trem', 'onibus', 'metro'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    stations = db.relationship('LineStation', backref='line', lazy=True, cascade='all, delete-orphan')
    status_reports = db.relationship('VehicleStatus', backref='line', lazy=True)
    
    def __repr__(self):
        return f'<TransportLine {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Station(db.Model):
    __tablename__ = 'stations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    lines = db.relationship('LineStation', backref='station', lazy=True)
    status_reports = db.relationship('VehicleStatus', backref='station', lazy=True)
    
    def __repr__(self):
        return f'<Station {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class LineStation(db.Model):
    __tablename__ = 'line_stations'
    
    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.Integer, db.ForeignKey('transport_lines.id'), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)  # Ordem da estação na linha
    
    def __repr__(self):
        return f'<LineStation line_id={self.line_id} station_id={self.station_id} order={self.order}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'line_id': self.line_id,
            'station_id': self.station_id,
            'order': self.order
        }

class VehicleStatus(db.Model):
    __tablename__ = 'vehicle_status'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    line_id = db.Column(db.Integer, db.ForeignKey('transport_lines.id'), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=True)
    status_type = db.Column(db.String(50), nullable=False)  # 'esperando', 'embarcado', 'cheio', 'parado', 'andando'
    message = db.Column(db.Text, nullable=True)  # Mensagem opcional do usuário
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref='status_reports', lazy=True)
    
    def __repr__(self):
        return f'<VehicleStatus {self.status_type} by user {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'line_id': self.line_id,
            'station_id': self.station_id,
            'status_type': self.status_type,
            'message': self.message,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'user': self.user.to_dict() if self.user else None,
            'station': self.station.to_dict() if self.station else None,
            'line': self.line.to_dict() if self.line else None
        }

