import os
import sqlite3
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Garante que a pasta 'instance/' exista
if not os.path.exists('instance'):
    os.makedirs('instance')
    print("Directory 'instance/' created successfully.")

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelo de usuário
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Função para carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('instance/tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1])
    return None

# Função para inicializar o banco de dados e criar as tabelas
def init_db():
    try:
        print("Starting database creation...")
        conn = sqlite3.connect('instance/tasks.db')
        cursor = conn.cursor()
        
        # Cria a tabela de usuários, se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        
        # Cria a tabela de tarefas, se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Adiciona um usuário padrão
        hashed_password = generate_password_hash('admin123', method='pbkdf2:sha256')
        cursor.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', ('admin', hashed_password))
        
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

# Inicializa o banco de dados antes da primeira requisição
@app.before_first_request
def initialize_database():
    init_db()
    
# Função para adicionar uma nova tarefa ao banco
def add_task_to_db(task_text, user_id):
    try:
        conn = sqlite3.connect('instance/tasks.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task, user_id) VALUES (?, ?)', (task_text, user_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error adding task: {e}")

# Função para buscar todas as tarefas do banco para um usuário
def get_tasks_from_db(user_id):
    try:
        conn = sqlite3.connect('instance/tasks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, task FROM tasks WHERE user_id = ?', (user_id,))
        tasks = cursor.fetchall()
        conn.close()
        return [{'id': task[0], 'task': task[1]} for task in tasks]
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []
    
# Rota para a página inicial
@app.route('/')
@login_required
def home():
    return render_template('index.html', username=current_user.username)

# Rota para manipular as tarefas (adicionar e listar)
@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks_handler():
    if request.method == 'GET':
        tasks = get_tasks_from_db(current_user.id)
        return jsonify(tasks)
    if request.method == 'POST':
        task_data = request.get_json()
        if not task_data or 'task' not in task_data:
            return jsonify({'error': 'Invalid data'}), 400
        add_task_to_db(task_data['task'], current_user.id)
        return jsonify({'task': task_data['task']}), 201
    
# Rota para deletar uma tarefa
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    try:
        conn = sqlite3.connect('instance/tasks.db')
        cursor = conn.cursor()
        
        # Verifica se a tarefa pertence ao usuário autenticado
        cursor.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (task_id, current_user.id))
        conn.commit()
        conn.close()
        
        return '', 204  # Retorna sucesso sem conteúdo
    except Exception as e:
        print(f"Error processing DELETE request: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Rota para registro de novos usuários
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validação de entrada
        if not username or not password or not confirm_password:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        # Verificar se o nome de usuário já existe
        conn = sqlite3.connect('instance/tasks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists. Please choose another.', 'error')
            conn.close()
            return render_template('register.html')

        # Adicionar o novo usuário ao banco de dados
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        flash('User registered successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Atualizar a rota de login para validação
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verificar credenciais no banco de dados
        conn = sqlite3.connect('instance/tasks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if not user or not check_password_hash(user[1], password):
            flash('Invalid credentials. Try again.', 'error')
            return render_template('login.html')

        # Autenticar o usuário
        login_user(User(user[0], username))
        return redirect(url_for('home'))

    return render_template('login.html')

# Rota para logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rota para verificar se o username já existe no banco de dados
@app.route('/check-username', methods=['GET'])
def check_username():
    username = request.args.get('username')
    if not username:
        return jsonify({'exists': False})

    try:
        conn = sqlite3.connect('instance/tasks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify({'exists': True})
        else:
            return jsonify({'exists': False})
    except Exception as e:
        print(f"Erro ao verificar username: {e}")
        return jsonify({'exists': False}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)