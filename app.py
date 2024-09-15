from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

tasks = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json.get('task')
    if task:
        tasks.append({'id': len(tasks) + 1, 'task': task})
        return jsonify({'message': 'Task added successfully!'}), 201
    return jsonify({'message': 'Task is required!'}), 400

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'message': 'Task deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
