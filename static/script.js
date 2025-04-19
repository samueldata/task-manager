// --- Funções gerais ---
async function loadTasks() {
    const taskList = document.getElementById('taskList');
    if (!taskList) return;  // só roda em index.html

    const response = await fetch('/tasks');
    if (!response.ok) {
        console.error('Erro ao carregar tarefas:', response.statusText);
        return;
    }
    const tasks = await response.json();
    taskList.innerHTML = '';

    tasks.forEach(task => {
        const li = document.createElement('li');
        li.textContent = task.task;
        li.dataset.id = task.id;
        li.classList.add('task-item');
        li.addEventListener('click', async () => {
            await deleteTask(task.id);
            loadTasks();
        });
        taskList.appendChild(li);
    });
}

async function deleteTask(taskId) {
    const response = await fetch(`/tasks/${taskId}`, { method: 'DELETE' });
    if (!response.ok) console.error('Erro ao deletar tarefa:', response.statusText);
}

async function logout() {
    const response = await fetch('/logout', { method: 'GET' });
    if (response.ok) {
        window.location.href = '/login';
    } else {
        console.error('Erro ao realizar logout');
    }
}

// --- DOMContentLoaded: só rodar depois do HTML carregado ---
document.addEventListener('DOMContentLoaded', () => {

    // 1) Toggle de tema (presente em index.html)
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            themeToggle.textContent = document.body.classList.contains('dark-mode') ? '🌜' : '🌞';
        });
    }

    // 2) Flash message (register & login)
    const flashContainers = document.querySelectorAll('.flash-container');
    flashContainers.forEach(flashContainer => {
        setTimeout(() => {
            flashContainer.style.opacity = '0';
            setTimeout(() => flashContainer.remove(), 500);
        }, 5000); // 5 segundos para desaparecer
    });

    // 3) Form de registro (register.html)
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm_password');
        const message = document.getElementById('message');
        const usernameInput = document.getElementById('username');
        const usernameMessage = document.getElementById('username-message');

        // Validação de senha
        function checkMatch() {
            if (password.value === confirmPassword.value) {
                message.textContent = 'Passwords match ✅';
                message.className = 'success';
                return true;
            } else {
                message.textContent = 'Passwords do not match ❌';
                message.className = 'error';
                return false;
            }
        }
        confirmPassword.addEventListener('input', checkMatch);
        registerForm.addEventListener('submit', e => {
            if (!checkMatch()) e.preventDefault();
        });

        // Validação de username via fetch
        async function checkUsernameExists(username) {
            try {
                const res = await fetch(`/check-username?username=${encodeURIComponent(username)}`);
                if (res.ok) {
                    const data = await res.json();
                    return data.exists;
                }
            } catch (err) {
                console.error('Error checking username:', err);
            }
            return false;
        }
        usernameInput.addEventListener('input', async () => {
            const uname = usernameInput.value.trim();
            if (!uname) {
                usernameMessage.textContent = '';
                usernameInput.classList.remove('error');
                return;
            }
            const exists = await checkUsernameExists(uname);
            if (exists) {
                usernameMessage.textContent = 'Username already exists ❌';
                usernameMessage.className = 'error';
                usernameInput.classList.add('error');
            } else {
                usernameMessage.textContent = 'Username is available ✅';
                usernameMessage.className = 'success';
                usernameInput.classList.remove('error');
            }
        });
    }

    // 4) Logout (index.html)
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }

    // 5) Task Manager (index.html)
    const taskForm = document.getElementById('taskForm');
    const taskInput = document.getElementById('taskInput');
    if (taskForm && taskInput) {
        taskForm.addEventListener('submit', async e => {
            e.preventDefault();
            const text = taskInput.value.trim();
            if (!text) return;
            const res = await fetch('/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task: text })
            });
            if (res.ok) {
                taskInput.value = '';
                loadTasks();
            } else {
                console.error('Erro ao adicionar tarefa:', res.statusText);
            }
        });
        loadTasks();  // carrega as tasks só aqui
    }

});
