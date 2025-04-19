// Função para carregar as tarefas
async function loadTasks() {
    const response = await fetch('/tasks');
    const tasks = await response.json();
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = ''; // Limpar a lista antes de carregar

    tasks.forEach(task => {
        const li = document.createElement('li');
        li.textContent = task.task;
        li.dataset.id = task.id;
        li.classList.add('task-item');

        // Adicionar função para deletar a tarefa ao clicar
        li.addEventListener('click', async () => {
            await deleteTask(task.id);
            loadTasks(); // Recarregar as tarefas
        });

        taskList.appendChild(li);
    });
}

// Função para deletar uma tarefa
async function deleteTask(taskId) {
    const response = await fetch(`/tasks/${taskId}`, {
        method: 'DELETE'
    });
    if (!response.ok) {
        console.error('Erro ao deletar tarefa:', response.statusText);
    }
}

// Função para realizar o logout
async function logout() {
    const response = await fetch('/logout', {
        method: 'GET'
    });
    if (response.ok) {
        // Redirecionar para a página de login após o logout
        window.location.href = '/login';
    } else {
        console.error('Erro ao realizar logout');
    }
}

// Alternar entre modos de tema claro/escuro
document.getElementById('themeToggle').addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const themeToggle = document.getElementById('themeToggle');
    themeToggle.textContent = document.body.classList.contains('dark-mode') ? '🌜' : '🌞';
});

// Adicionar eventos após o DOM ser carregado
document.addEventListener('DOMContentLoaded', () => {
    // Adicionar evento de clique ao botão de logout
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }

    // Adicionar evento ao formulário de adicionar tarefas
    const taskForm = document.getElementById('taskForm');
    if (taskForm) {
        taskForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const taskInput = document.getElementById('taskInput').value;
            const response = await fetch('/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ task: taskInput })
            });
            if (response.ok) {
                loadTasks(); // Recarregar as tarefas
                document.getElementById('taskInput').value = ''; // Limpar o input
            }
        });
    }

    // Carregar as tarefas ao carregar a página
    loadTasks();
});