import os
import sqlite3
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Garante que a pasta 'instance/' exista
if not os.path.exists('instance'):
    os.makedirs('instance')
    print("Diretório 'instance/' criado com sucesso.")

app = Flask(__name__)

# Initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Update Task model to include user_id
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Update the init_db function to hash passwords for initial users
def init_db():
    with app.app_context():
        db.create_all()
        # Example: Adding an initial user with a hashed password
        if not User.query.filter_by(username='admin').first():
            hashed_password = generate_password_hash('admin123', method='bcrypt')
            admin_user = User(username='admin', password=hashed_password)
            db.session.add(admin_user)
            db.session.commit()
        print("Database initialized.")

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
@login_required
def tasks_handler():
    if request.method == 'GET':
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return jsonify([{'id': task.id, 'title': task.title, 'description': task.description} for task in tasks])

    if request.method == 'POST':
        task_data = request.get_json()
        if not task_data or 'title' not in task_data:
            return jsonify({'error': 'Invalid data'}), 400

        new_task = Task(title=task_data['title'], description=task_data.get('description'), user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'id': new_task.id, 'title': new_task.title, 'description': new_task.description}), 201

# Rota para deletar uma tarefa
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found or unauthorized'}), 404

    db.session.delete(task)
    db.session.commit()
    return '', 204

# Rota para inicializar o banco de dados manualmente
@app.route('/init-db', methods=['GET'])
def initialize_database():
    try:
        init_db()
        return "Banco de dados inicializado com sucesso.", 200
    except Exception as e:
        return f"Erro ao inicializar o banco de dados: {e}", 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados ao iniciar o app
    app.run(debug=False, port=5001)