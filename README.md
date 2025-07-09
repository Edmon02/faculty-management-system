# Faculty Management System

**🚀 For comprehensive and detailed documentation, please visit our new [Documentation Hub](./docs/README.md)! 🚀**

A comprehensive web application for managing faculty information, including students, teachers, courses, and more. This system is designed to streamline communication and administrative tasks within an educational department.

## Overview

The Faculty Management System (FMS) provides a robust platform with features like:

*   User authentication and role-based access control (Admin, Lecturer, Student)
*   Management of Students, Teachers, Subjects, and Exercises
*   News publication and file handling
*   A "Waiting Room" feature for lecturers to review submissions
*   (Conceptual) Chatbot integration

For a full list and detailed explanations of features, please see the [Features & Functionality section in our docs](./docs/04_features.md).

## Getting Started

While the quick setup steps below are provided, we **highly recommend** following the detailed [**Getting Started Guide in our documentation**](./docs/01_getting_started.md) for comprehensive setup instructions, prerequisites, and important notes (especially regarding static assets).

### Basic Prerequisites

*   Python 3.8 or higher
*   Git

### Quick Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Edmon02/faculty-management-system.git
    cd faculty-management-system
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **(Optional) Create `.env` file:**
    Based on `.env.example` (if present) or for custom settings. See `docs/05_configuration.md`. For basic SQLite development, defaults may suffice.

5.  **Run the application:**
    ```bash
    python run.py
    ```
    The application should be available at `http://127.0.0.1:5000/`.

    **⚠️ Important Note on Static Assets:** For the application to render correctly with all styling and frontend features, static assets (CSS, JS, images for the theme, and React build artifacts) are required. These appear to be missing from the main repository. Please refer to the "Important Note on Static Assets" in the [full Getting Started guide](./docs/01_getting_started.md#important-note-on-static-assets) for more details.

## Project Structure

The project follows a modular Flask application structure. For a detailed breakdown, please see the [Architecture documentation](./docs/02_architecture.md#directory-structure).

## Development

*   **Database:** Uses SQLite by default for development (auto-created).
*   **Testing:** Run tests with `pytest`. See [Testing & Validation Guide](./docs/06_testing.md).
*   **Code Quality:** Check PEP 8 standards with `flake8`.

## Default User Accounts

For testing purposes, the following accounts are available (also listed in `docs/01_getting_started.md`):

*   **Admin:** Username: `fYRKVPTdzT`, Password: `03611557`
*   **Lecturer:** Username: `fYRKVPTdzm`, Password: `71319352`
*   **Student:** Username: `ElwAiWgAZg`, Password: `03611558`

## Contributing

We welcome contributions! Please see our detailed [**Contributing Guide**](./docs/08_contributing.md) for information on workflow, code standards, and how to help.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---
**Dive deeper! Explore the full [Faculty Management System Documentation](./docs/README.md).**
