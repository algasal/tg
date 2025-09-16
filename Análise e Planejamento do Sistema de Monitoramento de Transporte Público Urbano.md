
## Análise e Planejamento do Sistema de Monitoramento de Transporte Público Urbano

### 1. Funcionalidades Principais

O sistema de monitoramento de serviço de transporte público urbano, similar ao Waze, terá as seguintes funcionalidades principais:

*   **Relato de Status pelo Usuário:**
    *   **Localização:** Usuários podem compartilhar sua localização atual (plataforma, dentro do veículo).
    *   **Tempo de Espera:** Usuários podem informar há quanto tempo estão esperando.
    *   **Status do Veículo:** Usuários podem reportar o status do veículo (ex: 'embarcado', 'trem cheio', 'parado', 'andando').
    *   **Eventos:** Usuários podem reportar eventos específicos (ex: 'atraso', 'problema na linha').

*   **Monitoramento em Tempo Real:**
    *   **Visualização no Mapa:** Outros usuários podem visualizar a localização e o status dos veículos de transporte público em um mapa em tempo real.
    *   **Informações Detalhadas:** Exibição de informações como tempo estimado de chegada, lotação do veículo, e histórico de eventos.
    *   **Alertas:** Notificações sobre atrasos, interrupções ou mudanças de rota.

*   **Suporte à Decisão do Usuário:**
    *   **Comparação de Rotas:** Ferramenta para comparar o tempo de viagem e o status de diferentes opções de transporte (trem vs. ônibus).
    *   **Previsão de Impacto:** Estimativa do impacto de eventos reportados no tempo total de viagem.

*   **Autenticação e Perfil de Usuário:**
    *   Registro e login de usuários.
    *   Perfis de usuário para gerenciar rotas favoritas e preferências de notificação.

### 2. Arquitetura do Sistema

A arquitetura do sistema será dividida em três componentes principais:

*   **Frontend (Aplicação Web):** Interface do usuário para interação com o sistema.
*   **Backend (API RESTful):** Lógica de negócios, processamento de dados e comunicação com o banco de dados.
*   **Banco de Dados:** Armazenamento persistente de dados de usuários, veículos, rotas e eventos.

### 3. Tecnologias Propostas

*   **Backend:** Python com framework Flask (leve e flexível para APIs RESTful).
*   **Frontend:** React (biblioteca JavaScript para construção de interfaces de usuário interativas).
*   **Banco de Dados:** SQLite (para protótipo e desenvolvimento local, fácil de configurar e sem servidor) ou PostgreSQL (para escalabilidade futura).
*   **Mapeamento:** Integração com APIs de mapas (ex: Google Maps API, OpenStreetMap) para visualização em tempo real.
*   **Comunicação em Tempo Real:** WebSockets (para atualizações de status em tempo real do backend para o frontend).

### 4. Modelo de Dados Inicial

Serão consideradas as seguintes entidades:

*   **Usuário:** ID, nome, email, senha, localização atual.
*   **Veículo (Trem/Ônibus):** ID, tipo, linha, capacidade.
*   **Rota:** ID, nome, pontos de parada, veículos associados.
*   **Ponto de Parada:** ID, nome, localização (latitude, longitude).
*   **Status do Veículo:** ID, veículo_id, usuário_id, tipo_status (esperando, embarcado, cheio, parado, andando), timestamp, localização (latitude, longitude), mensagem (opcional).




### 5. Modelo de Dados Detalhado

Para o protótipo, usaremos um banco de dados SQLite. As tabelas principais serão:

#### Tabela `users`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `username` (TEXT NOT NULL UNIQUE)
- `password_hash` (TEXT NOT NULL)
- `email` (TEXT UNIQUE)
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

#### Tabela `transport_lines`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `name` (TEXT NOT NULL UNIQUE) - Ex: "Linha Vermelha", "Ônibus 101"
- `type` (TEXT NOT NULL) - Ex: "trem", "onibus"

#### Tabela `stations`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `name` (TEXT NOT NULL)
- `latitude` (REAL NOT NULL)
- `longitude` (REAL NOT NULL)

#### Tabela `line_stations` (Tabela de junção para rotas)
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `line_id` (INTEGER NOT NULL, FOREIGN KEY REFERENCES transport_lines(id))
- `station_id` (INTEGER NOT NULL, FOREIGN KEY REFERENCES stations(id))
- `order` (INTEGER NOT NULL) - Ordem da estação na linha

#### Tabela `vehicle_status`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `user_id` (INTEGER NOT NULL, FOREIGN KEY REFERENCES users(id))
- `line_id` (INTEGER NOT NULL, FOREIGN KEY REFERENCES transport_lines(id))
- `station_id` (INTEGER, FOREIGN KEY REFERENCES stations(id)) - Estação atual ou mais próxima
- `status_type` (TEXT NOT NULL) - Ex: "esperando", "embarcado", "cheio", "parado", "andando"
- `message` (TEXT) - Mensagem opcional do usuário (ex: "Trem parado há 5 minutos")
- `latitude` (REAL)
- `longitude` (REAL)
- `timestamp` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

Este modelo inicial permite registrar usuários, definir linhas de transporte e estações, e capturar atualizações de status dos veículos em tempo real, incluindo a localização e o tipo de status reportado pelo usuário. A flexibilidade do campo `status_type` e `message` permite acomodar os diferentes cenários descritos pelo usuário (esperando, cheio, parado, andando).

