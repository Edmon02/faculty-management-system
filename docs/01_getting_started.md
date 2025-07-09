# 1. Getting Started: Launching Your FMS Instance! 🚀

So, you're ready to roll up your sleeves and get the Faculty Management System (FMS) purring on your local machine? Excellent choice! This guide is your friendly co-pilot, designed to make the setup process as smooth as a perfectly optimized database query.

Think of this as assembling your very own FMS command center. By the end of this, you'll have a local version of the system running, ready for exploration, development, or just satisfying your curiosity.

## Prerequisites: Your Developer Toolkit 🛠️

Before we embark on this digital construction project, let's make sure your toolkit is ready. You'll need a few essential items:

*   **Python (The Engine):** Version 3.8 or higher. This is the programming language that powers FMS's backend.
    *   *Don't have it?* Grab it from [python.org](https://www.python.org/).
    *   *Check your version:* Open your terminal or command prompt and type `python --version` or `python3 --version`.
*   **pip (The Package Manager):** Python's trusty assistant for installing other software packages (it usually comes bundled with Python).
    *   *Check your version:* `pip --version` or `pip3 --version`.
*   **Git (The Time Machine & Collaborator):** Essential for downloading (cloning) the FMS codebase from its repository.
    *   *Need Git?* Download it from [git-scm.com](https://git-scm.com/).
    *   *Check your version:* `git --version`.
*   **(Highly Recommended!) Virtual Environment Tool (Your Project's Bubble):** Python's built-in `venv` module is perfect. This keeps FMS's specific software needs neatly separated from your other Python projects, preventing digital squabbles.
    *   *Curious if it's there?* `python -m venv --help` (or `python3 -m venv --help`).

**A Note on Databases:** For local development, FMS cleverly uses **SQLite**. This is a super convenient file-based database that Python manages directly – no separate database server installation needed to get started! If you were heading into the wilds of production, you'd likely want to set up something more heavy-duty like PostgreSQL, but for now, SQLite makes our lives easy.

## Setting Up for Local Development: Your Step-by-Step Adventure Guide 🗺️

Alright, toolkit checked! Let's bring FMS to life on your computer.

**Step 1: Clone the Mothership (Get the Code!)**

First, find a nice, organized spot on your computer for the FMS project. Then, open your terminal or command prompt and use Git to clone the repository:

```bash
git clone https://github.com/Edmon02/faculty-management-system.git
```
This downloads all the project files. Now, navigate into your newly created FMS directory:
```bash
cd faculty-management-system
```

**Step 2: Create Your Project's Bubble (Virtual Environment)**

This is where `venv` comes in. It's like creating a pristine, isolated workshop just for FMS.

*   **Craft the environment** (we'll call it `venv`, a common convention):
    ```bash
    python -m venv venv
    ```
    (If `python` doesn't work, try `python3`.)

*   **Activate the environment (Step into the bubble!):**
    *   On **macOS and Linux**:
        ```bash
        source venv/bin/activate
        ```
    *   On **Windows** (using Git Bash or PowerShell):
        ```bash
        venv\Scripts\activate
        ```
    *You'll know you're "in the bubble" when your command prompt changes to show `(venv)` at the beginning.* This means any Python or pip commands you run will be specific to this project.

**Step 3: Install the Gears (Project Dependencies)**

FMS relies on several Python packages (like Flask itself, SQLAlchemy for database magic, etc.). These are all listed in `requirements.txt`. Let's install them:

```bash
pip install -r requirements.txt
```
Pip will now read this file and download and install all the necessary components. Grab a cup of tea or coffee; this might take a moment! ☕

**Step 4: Configure Your Universe (Environment Variables - Optional for Basic Start)**

Applications often use environment variables for settings that might change between computers or environments (like secret keys or database locations).

*   **The `.env` File Approach:** Often, a project includes a `.env.example` file with templates for these variables. While not explicitly confirmed for this repository during initial analysis, if you found one, you'd copy it to a new file named `.env`:
    ```bash
    # If .env.example exists:
    # cp .env.example .env
    ```
    Then you'd edit `.env` with your specific settings. **Remember: `.env` files should *never* be committed to Git if they contain secrets!**

*   **FMS Defaults:** For FMS, critical settings like the `SECRET_KEY` and the `SQLALCHEMY_DATABASE_URI` (for SQLite) have sensible defaults in `app/config.py`. This means for a basic local SQLite setup, you might not need a `.env` file to get started.
*   **If you *do* want to override defaults**, you can create a `.env` file in the project's root directory. Here's an example of what it might contain:
    ```env
    # Example .env content (optional for basic SQLite setup)
    FLASK_CONFIG=development  # Ensures development settings are used
    SECRET_KEY='a_very_long_random_and_super_secret_string_that_you_invent' # Good for session stability
    # DATABASE_URL=sqlite:///my_custom_fms_dev.sqlite # If you want to name your DB file differently
    ```

**Step 5: The Database Awakens! (Automatic Initialization)**

Good news! FMS is designed to be user-friendly here. The application will automatically create the SQLite database file (e.g., `app/pulpit.sqlite`) and set up all the necessary tables the first time it starts. This magic happens thanks to `db.create_all()` in `app/__init__.py`. No complex database incantations required from you!

**Step 6: Ignite the Engines! (Run the Application)**

This is the moment of truth! You're all set to start the Flask development server.

In your terminal (make sure your `(venv)` is still active and you're in the `faculty-management-system` directory):
```bash
python run.py
```
Alternatively, if you prefer using the Flask CLI (you might need to set `FLASK_APP=run.py` as an environment variable or in your `.env` file for this to work directly):
```bash
flask run
```

If all goes well, you should see output indicating the server is running, typically something like:
```
 * Serving Flask app 'app' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: ...
```

**You've done it!** Your local FMS instance should now be accessible in your web browser at: `http://127.0.0.1:5000/`

**Pro Tip: Peeking at the Live Demo**
For reference, or just to see what a fully operational FMS looks like (with all its bells and whistles, including styling!), you can always visit the live public demo: [https://dante02.pythonanywhere.com/](https://dante02.pythonanywhere.com/)

## Quick Start: Your First Steps Inside FMS (Logging In)

With the server humming along locally:

1.  Open your favorite web browser and navigate to `http://127.0.0.1:5000/`. You should be greeted by the React-based landing page.
2.  To explore the authenticated areas (dashboards, management tools), you'll need to log in. Look for a "Login" link or button (typically on the landing page, or you can try navigating directly to `/login`).
3.  Use the provided default credentials to get started (we'll dive deeper into roles in the [Features](./04_features.md#user-authentication--roles) section):
    *   **Admin Account:**
        *   Username: `fYRKVPTdzT`
        *   Password: `03611557`
    *   **Lecturer Account:**
        *   Username: `fYRKVPTdzm`
        *   Password: `71319352`
    *   **Student Account:**
        *   Username: `ElwAiWgAZg`
        *   Password: `03611558`

## 🚨 Houston, We Have a Stylist... Or Do We? (Important Note on Static Assets!)

This is a crucial heads-up for your local development journey!

During our deep dive into the FMS repository, we noticed that some key ingredients for the visual presentation seem to be on a little vacation from the GitHub repo. Specifically, the static assets for:

*   The Flask application's theme (CSS, JavaScript, images usually found in `app/static/css/`, `app/static/js/`, etc.)
*   The React landing page's build artifacts (`app/static/react/`)

**What this means for your local setup:**

If you're running the application *solely* from the code cloned from the repository, you might find that:
*   The authenticated parts of the app (dashboards, forms, lists) look a bit... bare. Think of a house with great architecture but no paint or furniture. The functionality should largely be there, but the visual styling might be missing.
*   Some JavaScript-driven UI enhancements in the Flask/Jinja2 part might not work as expected.
*   The React landing page itself might not load correctly if its essential CSS and JS bundles are absent.

**How to navigate this cosmic anomaly:**

1.  **The Live Demo is Your North Star:** The public demo at [https://dante02.pythonanywhere.com/](https://dante02.pythonanywhere.com/) *does* have all these assets, so it's the best reference for the intended look and feel.
2.  **Seek the Missing Pieces:** The most straightforward solution is to **kindly ask the project owner for these missing static asset directories or for instructions on how to build/generate them.** There might be a separate build step for the frontend theme or the React app that isn't documented in the main repository.
3.  **Focus on Functionality:** Without these assets, your local development will be an excellent environment for working on backend logic (Python/Flask code), database interactions, API development, and HTML structure (Jinja2 templating). Visual perfection will have to wait until the assets are in place.

Don't let this deter you! The core engine of FMS is still there to explore.

## Troubleshooting Tips: When a Gremlin Appears 👾

Even the best of us hit snags. Here are a few common ones:

*   **"Help! `ModuleNotFoundError`!"**
    *   *The usual suspect:* Your virtual environment (`venv`) isn't active. Remember to `source venv/bin/activate` (or `venv\Scripts\activate` on Windows) in every new terminal session where you want to work on FMS.
    *   *Another possibility:* You might have missed `pip install -r requirements.txt`.
*   **"My Database is Acting Weird!"**
    *   For a fresh SQLite setup, this is rare. But if you suspect corruption or just want a clean slate, you *can* delete the SQLite database file (e.g., `app/pulpit.sqlite`). The app will try to recreate it on the next run.
    *   **⚠️ Extreme Caution:** Deleting the database file means **ALL DATA IS LOST**. Only do this if you're okay with starting fresh.
*   **"Port `5000` is Already in Use! Someone's squatting on my port!"**
    *   No worries! Another application on your computer is using that port. You can easily tell Flask to use a different one:
        *   Option 1: `python run.py --port 5001` (if `run.py` is set up to parse arguments, which it isn't by default).
        *   Option 2 (More reliable): Modify `run.py` temporarily: `app.run(debug=True, port=5001)`.
        *   Option 3 (Flask CLI): `flask run --port=5001`.

You should now have a functional (albeit potentially unstyled) local instance of the Faculty Management System. Dive in, explore, and happy developing! If you encounter other issues, the [FAQ section](./09_faq_glossary.md) or the project's GitHub Issues page might hold answers.
