import os
import sqlite3
from flask import Flask, jsonify, request, render_template

# Garante que a pasta 'instance/' exista
if not os.path.exists('instance'):
    os.makedirs('instance')
    print("Diretório 'instance/' criado com sucesso.")

app = Flask(__name__)

# Função para inicializar o banco de dados e criar a tabela de tarefas
def init_db():
    try:
        print("Iniciando a criação do banco de dados...")
        conn = sqlite3.connect('instance/tasks.db')  # Conecta ao banco
        cursor = conn.cursor()
        
        # Cria a tabela de tarefas, se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL
            )
        ''')
        print("Tabela 'tasks' criada ou já existente.")
        
        conn.commit()  # Salva as mudanças
        conn.close()   # Fecha a conexão
        print("Banco de dados inicializado com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

# Função para adicionar uma nova tarefa ao banco
def add_task_to_db(task_text):
    try:
        conn = sqlite3.connect('instance/tasks.db')
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task_text,))
        
        conn.commit()
        conn.close()
        print(f"Tarefa '{task_text}' adicionada com sucesso.")
    except Exception as e:
        print(f"Erro ao adicionar tarefa: {e}")

# Função para buscar todas as tarefas do banco
def get_tasks_from_db():
    try:
        conn = sqlite3.connect('instance/tasks.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()  # Retorna todas as tarefas como uma lista de tuplas
        
        conn.close()
        print("Tarefas recuperadas com sucesso.")
        return [{'id': task[0], 'task': task[1]} for task in tasks]  # Converte as tuplas em dicionários
    except Exception as e:
        print(f"Erro ao buscar tarefas: {e}")
        return []

# Função para excluir uma tarefa do banco
def delete_task_from_db(task_id):
    try:
        conn = sqlite3.connect('instance/tasks.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        
        conn.commit()
        conn.close()
        print(f"Tarefa com ID {task_id} excluída com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir tarefa: {e}")

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota para manipular as tarefas (adicionar e listar)
@app.route('/tasks', methods=['GET', 'POST'])
def tasks_handler():
    if request.method == 'GET':
        tasks = get_tasks_from_db()  # Pega as tarefas do banco
        return jsonify(tasks)
    
    if request.method == 'POST':
        try:
            task_data = request.get_json()
            if not task_data or 'task' not in task_data:
                return jsonify({'error': 'Invalid data'}), 400
            
            task_text = task_data.get('task')
            add_task_to_db(task_text)  # Adiciona a tarefa ao banco
            return jsonify({'task': task_text}), 201
        except Exception as e:
            print(f"Erro ao processar requisição POST: {e}")
            return jsonify({'error': 'Internal Server Error'}), 500

# Rota para deletar uma tarefa
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        delete_task_from_db(task_id)  # Deleta a tarefa do banco
        return '', 204
    except Exception as e:
        print(f"Erro ao processar requisição DELETE: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Rota para inicializar o banco de dados manualmente
@app.route('/init-db', methods=['GET'])
def initialize_database():
    try:
        init_db()
        return "Banco de dados inicializado com sucesso.", 200
    except Exception as e:
        return f"Erro ao inicializar o banco de dados: {e}", 500

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados ao iniciar o app
    app.run(debug=False, port=5001)