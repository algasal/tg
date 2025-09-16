"""
Script para popular o banco de dados com dados de exemplo
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db, User
from src.models.transport import TransportLine, Station, LineStation, VehicleStatus
from src.main import app

def seed_database():
    """Popula o banco de dados com dados de exemplo"""
    with app.app_context():
        # Limpa dados existentes
        VehicleStatus.query.delete()
        LineStation.query.delete()
        Station.query.delete()
        TransportLine.query.delete()
        User.query.delete()
        
        # Cria usuários de exemplo
        users = [
            {'username': 'joao_silva', 'email': 'joao@email.com', 'password': '123456'},
            {'username': 'maria_santos', 'email': 'maria@email.com', 'password': '123456'},
            {'username': 'pedro_oliveira', 'email': 'pedro@email.com', 'password': '123456'},
        ]
        
        user_objects = []
        for user_data in users:
            user = User(username=user_data['username'], email=user_data['email'])
            user.set_password(user_data['password'])
            user_objects.append(user)
            db.session.add(user)
        
        # Cria linhas de transporte
        lines = [
            {'name': 'Linha Vermelha', 'type': 'metro'},
            {'name': 'Linha Azul', 'type': 'metro'},
            {'name': 'Ônibus 101', 'type': 'onibus'},
            {'name': 'Trem Expresso', 'type': 'trem'},
        ]
        
        line_objects = []
        for line_data in lines:
            line = TransportLine(name=line_data['name'], type=line_data['type'])
            line_objects.append(line)
            db.session.add(line)
        
        # Cria estações
        stations = [
            # Linha Vermelha
            {'name': 'Estação Central', 'latitude': -23.5505, 'longitude': -46.6333},
            {'name': 'Estação Norte', 'latitude': -23.5405, 'longitude': -46.6233},
            {'name': 'Estação Sul', 'latitude': -23.5605, 'longitude': -46.6433},
            
            # Linha Azul
            {'name': 'Terminal Oeste', 'latitude': -23.5455, 'longitude': -46.6383},
            {'name': 'Estação Leste', 'latitude': -23.5555, 'longitude': -46.6283},
            
            # Pontos de ônibus
            {'name': 'Ponto Shopping', 'latitude': -23.5525, 'longitude': -46.6353},
            {'name': 'Ponto Universidade', 'latitude': -23.5475, 'longitude': -46.6303},
            
            # Estações de trem
            {'name': 'Terminal Rodoviário', 'latitude': -23.5585, 'longitude': -46.6403},
            {'name': 'Estação Aeroporto', 'latitude': -23.5425, 'longitude': -46.6253},
        ]
        
        station_objects = []
        for station_data in stations:
            station = Station(
                name=station_data['name'],
                latitude=station_data['latitude'],
                longitude=station_data['longitude']
            )
            station_objects.append(station)
            db.session.add(station)
        
        db.session.commit()
        
        # Associa estações às linhas
        line_station_associations = [
            # Linha Vermelha (id=1)
            {'line_id': 1, 'station_id': 1, 'order': 1},  # Estação Central
            {'line_id': 1, 'station_id': 2, 'order': 2},  # Estação Norte
            {'line_id': 1, 'station_id': 3, 'order': 3},  # Estação Sul
            
            # Linha Azul (id=2)
            {'line_id': 2, 'station_id': 4, 'order': 1},  # Terminal Oeste
            {'line_id': 2, 'station_id': 1, 'order': 2},  # Estação Central (compartilhada)
            {'line_id': 2, 'station_id': 5, 'order': 3},  # Estação Leste
            
            # Ônibus 101 (id=3)
            {'line_id': 3, 'station_id': 6, 'order': 1},  # Ponto Shopping
            {'line_id': 3, 'station_id': 7, 'order': 2},  # Ponto Universidade
            
            # Trem Expresso (id=4)
            {'line_id': 4, 'station_id': 8, 'order': 1},  # Terminal Rodoviário
            {'line_id': 4, 'station_id': 1, 'order': 2},  # Estação Central (compartilhada)
            {'line_id': 4, 'station_id': 9, 'order': 3},  # Estação Aeroporto
        ]
        
        for assoc in line_station_associations:
            line_station = LineStation(
                line_id=assoc['line_id'],
                station_id=assoc['station_id'],
                order=assoc['order']
            )
            db.session.add(line_station)
        
        # Cria alguns status de exemplo
        status_examples = [
            {
                'user_id': 1,
                'line_id': 1,
                'station_id': 1,
                'status_type': 'esperando',
                'message': 'Esperando há 5 minutos na plataforma',
                'latitude': -23.5505,
                'longitude': -46.6333
            },
            {
                'user_id': 2,
                'line_id': 1,
                'station_id': 2,
                'status_type': 'embarcado',
                'message': 'Trem está cheio, mas andando',
                'latitude': -23.5405,
                'longitude': -46.6233
            },
            {
                'user_id': 3,
                'line_id': 3,
                'station_id': 6,
                'status_type': 'parado',
                'message': 'Ônibus parado no trânsito há 10 minutos',
                'latitude': -23.5525,
                'longitude': -46.6353
            }
        ]
        
        for status_data in status_examples:
            status = VehicleStatus(**status_data)
            db.session.add(status)
        
        db.session.commit()
        print("Banco de dados populado com sucesso!")
        print(f"Criados: {len(users)} usuários, {len(lines)} linhas, {len(stations)} estações")

if __name__ == '__main__':
    seed_database()

