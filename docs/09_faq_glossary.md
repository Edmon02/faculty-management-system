# 9. FAQ & Glossary: Your FMS Decoder Ring ❓📖

Welcome to the FMS knowledge vault! This section is your go-to for quick answers to **Frequently Asked Questions (FAQ)** and a handy **Glossary** to decode any jargon or project-specific terms you might encounter. Think of it as your personal FMS encyclopedia and troubleshooter, rolled into one.

## Frequently Asked Questions (FAQ) - Your Burning Questions Answered! 🔥

Here are some common queries that might pop up as you explore or work with the Faculty Management System:

**Q1: Help! I've cloned the FMS repository, fired up the local server, but the pages look like a Picasso painting gone wrong – all unstyled and parts seem broken. What gives?**

**A1:** Ah, the classic "Where's my CSS?" conundrum! This is almost certainly due to **missing static assets**.
    *   **The Lowdown:** As highlighted in our [Getting Started Guide (Static Asset Alert!)](./01_getting_started.md#important-note-on-static-assets) and the [Architecture Deep Dive](./02_architecture.md#directory-structure), the vital CSS stylesheets, JavaScript files for the theme, images, and the React landing page's compiled build artifacts seem to have played hooky from the GitHub repository.
    *   **The Fix:**
        1.  The best course of action is to **reach out to the project owner/maintainer**. They likely have these asset directories (usually `app/static/css/`, `app/static/js/`, `app/static/images/`, and `app/static/react/`) or can provide instructions on how to generate them (e.g., if there's a separate frontend build process).
        2.  The live demo is your visual guide to what it *should* look like.
    *   **In the Meantime:** Without these assets, your local FMS instance will function primarily at the backend logic and HTML structure level. The full visual experience will be on hold until the assets are in place.

**Q2: I see `app/templates/index.html` and then a bunch of other `.html` files in `app/templates/`. What's the difference? Is `index.html` special?**

**A2:** Excellent question! They serve very different purposes:
    *   📄 **`app/templates/index.html` (The React Welcome Mat):** This file is **NOT** a standard Jinja2 template that Flask fills with dynamic data from Python. Instead, it's a relatively static HTML shell. Its main job is to be the **entry point for the public-facing landing page, which is built using React.** It typically contains a single `<div id="root"></div>` and `<script>` tags that load the compiled JavaScript and CSS bundles for the React application. Flask just serves this file as-is to the browser.
    *   📑 **Other `.html` Files (e.g., `base.html`, `students.html`, `dashboard.html` - The Jinja2 Workhorses):** These **ARE** Jinja2 templates. Flask processes them on the server. Python controller functions pass data (like lists of students, user details, etc.) to these templates, and Jinja2's templating language (`{{ variable }}`, `{% for item in list %}`, etc.) dynamically generates the final HTML that gets sent to the user's browser. These are for the authenticated parts of FMS – the dashboards, management pages, and so on. They almost always `{% extends "base.html" %}`.

**Q3: How does FMS handle who gets to see what? (Role-Based Access Control - RBAC)**

**A3:** FMS has a multi-layered security approach to ensure users only access appropriate information and features:
    1.  **Session Superpowers:** When a user logs in, their role (e.g., 'admin', 'lecturer', 'student') and unique ID are securely stored in their session. This is like their digital ID badge.
    2.  **The `@login_required` Doorman:** Many routes are protected by a `@login_required` decorator (or similar). If you're not logged in, you can't even get past the front door for these pages.
    3.  **The VIP Guest List (`RESTRICTED_ROUTES` in `app/config.py`):** This Python dictionary is a crucial part of FMS's access control. It lists specific URL paths that certain roles (like 'student' or 'lecturer') are explicitly *not* allowed to visit (e.g., admin-only pages).
    4.  **The Bouncer (`app/utils/security.py` - `check_restricted_route`):** This utility function, typically triggered automatically before each request (via a `before_request` hook), consults the `RESTRICTED_ROUTES` list. If a user tries to access a page their role isn't permitted for, this function can block access (e.g., show an error or redirect them).
    5.  **Smart Templates (Conditional Logic):** Even within pages, Jinja2 templates use session information (like `session['type'] == 'admin'`) to conditionally show or hide specific buttons, links, or sections of content. For example, the "Add New Student" button will only appear if an admin is logged in.

**Q4: I want to add a new Python library/package to FMS. What's the process?**

**A4:** Easy peasy! Here's the standard FMS pitstop procedure:
    1.  **Activate Your Bubble:** Make sure your Python virtual environment is active (`source venv/bin/activate` or `venv\Scripts\activate`).
    2.  **Install with Pip:** Use pip to install the new package: `pip install cool-new-package-name`.
    3.  **Update the Shopping List:** Add this new dependency (and its version) to your `requirements.txt` file. The easiest way is: `pip freeze > requirements.txt`. This command overwrites the file with *all* packages currently in your virtual environment.
    4.  **Commit the Change:** Add the updated `requirements.txt` to your Git commit. This ensures other developers (and your future self) will install the same dependencies.

**Q5: Where does FMS keep its main "brain" – the business logic?**

**A5:** The core business logic (the "how-to" for complex operations) is primarily encapsulated in the **service layer**. You'll find these service classes in the `app/services/` directory (e.g., `StudentService`, `AuthService`, `ExerciseService`). Controllers (`app/controllers/`) act as dispatchers, receiving user requests and then calling methods on these services to get the actual work done. This design keeps controllers lean and makes the business logic reusable and easier to test.

**Q6: I prefer PostgreSQL/MySQL for development over SQLite. Can I switch?**

**A6:** Absolutely! While SQLite is fantastic for getting started quickly (no separate server needed!), FMS is built with SQLAlchemy, which is database-agnostic. To switch:
    1.  **Install Your DB Server:** Make sure PostgreSQL or MySQL (or your preferred SQL database) is installed and running on your system.
    2.  **Get the Python Driver:** Install the appropriate Python adapter for your database using pip (e.g., `pip install psycopg2-binary` for PostgreSQL, or `pip install mysqlclient` for MySQL). Don't forget to add it to `requirements.txt`!
    3.  **Update the Connection String:** The crucial step! You'll need to tell SQLAlchemy how to connect to your new database. You can do this by:
        *   Modifying `SQLALCHEMY_DATABASE_URI` in the `DevelopmentConfig` class within `app/config.py`.
        *   Or, even better (especially if you want to keep your config file clean), set the `DATABASE_URL` environment variable in your `.env` file.
        *   *Example for PostgreSQL:* `DATABASE_URL='postgresql://your_user:your_password@localhost:5432/your_fms_dev_db'`
    4.  **DB Server Running?** Ensure your database server is active before you try to run the FMS application.

**Q7: I see files like `pulpit.sqlite` in the `app/` directory in the repository. What are they, and should they be there?**

**A7:** That `*.sqlite` file (e.g., `app/pulpit.sqlite`) is the **SQLite database file itself**. SQLite stores the entire database (all tables, data, etc.) in a single file.
    *   `pulpit.sqlite` is likely the default development database that gets automatically created when you first run the application.
    *   **Should it be in the Git repository?** Generally, **no**. Database files often contain test data or local development data that isn't relevant to other developers and can bloat the repository. It's standard practice to add `*.sqlite` (or specific database file names) to your project's `.gitignore` file. The only exception might be if it's a pre-populated, read-only database intended for demos or specific test scenarios.

**Q8: The original `CONTRIBUTING.md` mentioned PostgreSQL and Redis as prerequisites, but the app starts up with just Python and SQLite. What's the deal?**

**A8:** That's a good observation! The original `CONTRIBUTING.md` might have been written with an ideal or target production environment in mind, or perhaps for a version of the project that had features relying more heavily on those services.
    *   The FMS codebase, as it currently stands and is configured for development (`DevelopmentConfig`), defaults to using SQLite for the database.
    *   Similarly, while Redis is excellent for things like caching or as a backend for rate limiting in production, the default development configuration for rate limiting in FMS is set up to work without an external Redis server (likely using an SQLite-based or in-memory store for dev).
    *   So, for basic local development and contributing to many of the core Flask backend features, just Python and the automatically created SQLite database are sufficient to get you started! PostgreSQL and Redis would become more important if you were setting up a production-like environment or working on specific advanced features that explicitly require them.

## Glossary: Your FMS Lingua Franca 🗣️

Navigating a new codebase can sometimes feel like learning a new language. Here are some common terms and FMS-specific concepts:

*   **API (Application Programming Interface):** A contract that allows different software components to talk to each other. In FMS, some Flask routes might act as API endpoints, often returning data in JSON format for use by JavaScript or other services.
*   **Blueprint (Flask):** A way to organize a Flask application into a collection of smaller, manageable, and reusable "mini-applications." Each blueprint can have its own set of routes, templates, and static files. FMS uses blueprints to group features like authentication (`auth_bp`), student management (`students_bp`), etc. You'll find them in `app/routes/`.
*   **Controller:** In FMS's architecture (which loosely follows MVC), controllers are the Python classes or functions (often in `app/controllers/`) that handle incoming web requests routed by Blueprints. They process input, interact with services to perform business logic, and then decide what response to send back (usually by rendering an HTML template).
*   **CSRF (Cross-Site Request Forgery):** A common web security attack. FMS uses Flask-WTF's `CSRFProtect` extension, which typically involves adding a hidden token to forms to ensure that requests are legitimate and originate from the application itself.
*   **Decorator (Python):** A special syntax in Python (using the `@` symbol) to modify or enhance functions or methods. Flask uses decorators extensively: `@app.route()` or `@blueprint.route()` to link functions to URLs, and custom decorators like `@login_required` to add security checks.
*   **Environment Variables:** Configuration settings that live outside your application code (e.g., in your operating system's environment or loaded from a `.env` file). They allow you to customize app behavior (like `SECRET_KEY` or `DATABASE_URL`) without changing the code itself.
*   **Flask:** The Python micro-framework that FMS is built upon. It provides the core tools for handling web requests, routing, sessions, and more.
*   **Git:** The distributed version control system we use to track every change to the FMS codebase. It's like an infinite "undo" button and a collaboration superpower.
*   **GitHub:** The web platform where the FMS code is hosted, and where we collaborate using Git (e.g., through Pull Requests and Issues).
*   **Jinja2:** The powerful templating engine used by Flask. It allows us to embed Python-like expressions and logic within our HTML files (`app/templates/`) to generate dynamic web pages.
*   **JSON (JavaScript Object Notation):** A human-readable, lightweight format for exchanging data. Often used by APIs.
*   **Landing Page:** The very first page a user typically sees when they visit the FMS website's main URL. In FMS, this is a modern, interactive page built with React.
*   **Linting:** The process of using an automated tool (a "linter") to analyze source code for potential errors, bugs, stylistic inconsistencies, and code quality issues. FMS uses `flake8` for Python code.
*   **Macro (Jinja2):** Reusable pieces of Jinja2 template code, much like functions in Python. FMS uses a powerful macro in `app/templates/includes/_forms.html` (`render_form_field`) to generate standard HTML for various form input fields, keeping our forms consistent and DRY (Don't Repeat Yourself).
*   **Migration (Database):** When you change your database structure (e.g., add a new table or a column to an existing table), a "migration" is the process of applying those changes to an existing database without losing data. Tools like Alembic (often used with the Flask-Migrate extension) automate this. (While FMS uses `db.create_all()` for initial setup, a full migration system would be essential for evolving a production database).
*   **Model (MVC/ORM):** In FMS, these are Python classes (defined in `app/models/`) that represent the structure of our data and how it's stored in the database. They are built using SQLAlchemy.
*   **ORM (Object-Relational Mapper):** A programming technique that converts data between incompatible type systems using object-oriented programming languages. SQLAlchemy is the ORM FMS uses, allowing us to interact with database tables and rows as if they were Python objects and attributes.
*   **PaaS (Platform as a Service):** A type of cloud computing service that provides a platform allowing customers to develop, run, and manage applications without the complexity of building and maintaining the infrastructure typically associated with it. PythonAnywhere (where the FMS demo is hosted) is an example.
*   **PEP 8:** The official style guide for Python code, outlining conventions for formatting, naming, and writing readable Python.
*   **Pytest:** The testing framework used by FMS to write and run automated tests for the backend Python code.
*   **React:** A popular JavaScript library for building user interfaces, especially Single Page Applications (SPAs). FMS uses React for its public landing page and potentially for embedded UI components.
*   **Refactoring:** The process of restructuring existing computer code – changing its internal structure – without changing its external behavior or functionality. We did a fair bit of this with the FMS HTML templates to improve their organization and reduce repetition!
*   **Route:** A specific URL pattern (e.g., `/students/add`) that is mapped to a particular Python function (a view function or controller action) in a web application.
*   **Service Layer:** An architectural pattern where the main business logic of the application is placed in separate "service" classes or modules (found in `app/services/`). These services mediate between the web request handlers (controllers) and the data access layer (models).
*   **Session (Web):** A mechanism to store information about a user across multiple requests. When you log into FMS, your user ID and role are stored in a session, so the system remembers who you are as you navigate from page to page. Flask typically uses cryptographically signed cookies to store session data on the client-side.
*   **SPA (Single Page Application):** A web application that loads a single HTML page and then dynamically updates content as the user interacts with the app, usually by fetching data from a server via APIs. The FMS landing page is an SPA built with React.
*   **SQLite:** A C-language library that provides a lightweight, file-based SQL database engine. It's self-contained, serverless, and requires no configuration, making it excellent for development and testing, which is how FMS uses it by default.
*   **SQLAlchemy:** A powerful SQL toolkit and Object-Relational Mapper (ORM) for Python. It gives FMS developers the ability to work with databases using Python objects and methods instead of writing raw SQL queries for everything.
*   **Static Assets:** Files like CSS, JavaScript, images, and fonts that are served directly to the user's browser without any server-side processing. In FMS, these are intended to be stored in the `app/static/` directory.
*   **Template Engine:** Software that takes a template file (like a Jinja2 `.html` file with special placeholders and logic) and data, and processes them to produce a final output document (usually a complete HTML page).
*   **Virtual Environment (Python):** A self-contained directory tree that includes a Python installation for a particular version of Python, plus a number of additional packages. It allows you to work on different projects with different dependencies without them interfering with each other. `venv` is the standard tool for this.
*   **WSGI (Web Server Gateway Interface):** A standard specification for how web servers in Python should communicate with web applications or frameworks like Flask. Production-grade servers like Gunicorn or uWSGI are WSGI servers that run your Flask app.
