import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Função para inicializar o banco de dados e criar a tabela de tarefas
def init_db():
    conn = sqlite3.connect('instance/tasks.db')  # Conecta ao banco
    cursor = conn.cursor()
    
    # Cria a tabela de tarefas, se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    ''')
    
    conn.commit()  # Salva as mudanças
    conn.close()   # Fecha a conexão

# Função para adicionar uma nova tarefa ao banco
def add_task_to_db(task_text):
    conn = sqlite3.connect('instance/tasks.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task_text,))
    
    conn.commit()
    conn.close()

# Função para buscar todas as tarefas do banco
def get_tasks_from_db():
    conn = sqlite3.connect('instance/tasks.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()  # Retorna todas as tarefas como uma lista de tuplas
    
    conn.close()
    return [{'id': task[0], 'task': task[1]} for task in tasks]  # Converte as tuplas em dicionários

# Função para excluir uma tarefa do banco
def delete_task_from_db(task_id):
    conn = sqlite3.connect('instance/tasks.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    
    conn.commit()
    conn.close()

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
        task_data = request.get_json()
        task_text = task_data.get('task')
        add_task_to_db(task_text)  # Adiciona a tarefa ao banco
        return jsonify({'task': task_text}), 201

# Rota para deletar uma tarefa
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    delete_task_from_db(task_id)  # Deleta a tarefa do banco
    return '', 204

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados ao iniciar o app
    app.run(debug=True, port=5001)
