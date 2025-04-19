# Task Manager

![License: MIT](https://img.shields.io/github/license/samueldata/task-manager)   ![Python Version](https://img.shields.io/badge/python-3.9.7-blue)   ![Last Commit](https://img.shields.io/github/last-commit/samueldata/task-manager)   ![GitHub issues](https://img.shields.io/github/issues/samueldata/task-manager)   ![Repo Size](https://img.shields.io/github/repo-size/samueldata/task-manager)   ![GitHub forks](https://img.shields.io/github/forks/samueldata/task-manager?style=social)   ![GitHub stars](https://img.shields.io/github/stars/samueldata/task-manager?style=social)

![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)

A fully functional task manager application built with Flask. This project includes user authentication, task management, and a responsive UI. It is a great starting point for anyone looking to create a task management system and is open to contributions and improvements.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Demonstration](#demonstration)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **User Authentication**:
  - Login and logout functionality.
  - Tasks are user-specific and private.
- **Task Management**:
  - Add new tasks.
  - View all tasks.
  - Delete tasks.
- **Persistent Data**:
  - Tasks are stored in a SQLite database and persist across sessions.
- **Responsive UI**:
  - Simple and intuitive design.
  - Toggle between light and dark themes.
- **Secure Passwords**:
  - Passwords are hashed using `pbkdf2:sha256` for security.

---

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/samueldata/task-manager.git
    cd task-manager
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the database**:
    Ensure the `instance` directory exists and the SQLite database is initialized:
    ```bash
    python app.py
    ```

5. **Run the application**:
    ```bash
    python app.py
    ```

6. **Open your browser and navigate to**:
    ```
    http://127.0.0.1:5001
    ```

---

## Usage

- **Login**:
  - Use the default credentials:
    - **Username**: `admin`
    - **Password**: `admin123`
  - Or create a new user in the database.
- **Home Page**:
  - View and manage your tasks.
- **Add Task**:
  - Use the input field to add a new task.
- **Delete Task**:
  - Click on a task to delete it.
- **Logout**:
  - Use the logout button (🔓) in the top-right corner to log out.

---

## Demonstration

### Login Page
![Login Page](https://github.com/user-attachments/assets/6d460b77-aa84-4915-bb0e-091ce8b89cb4)

### Task Manager
![Task Manager](https://github.com/user-attachments/assets/c640f797-023c-4c35-a79f-e3854c787b52)

---

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Environment Management**: Virtualenv

---

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

Please make sure your code follows the project's coding standards and includes tests if applicable.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

If you have any questions or suggestions, feel free to reach out:

- **Email**: datasamuel@outlook.com
- **GitHub**: [samueldata](https://github.com/samueldata)

---

Happy coding! 😊
