# 8. Contributing to the Faculty Management System: Join the FMS Crew! 🤝

So, you've explored the Faculty Management System (FMS), and now you're thinking, "Hey, I could help make this even better!" That's fantastic! We're thrilled you're interested in contributing. Whether you're a seasoned developer ready to tackle a complex feature, a keen-eyed bug hunter, a documentation wizard, or someone with a great idea for improvement, your input is incredibly valuable.

This guide is your map and compass for navigating the contribution process. Let's build something great together!

## Our Guiding Principles: The FMS Contributor's Creed 📜

Contributing to any collaborative project, especially one like FMS, is a team sport. We believe in a few core principles to make it a rewarding experience for everyone:

*   🗣️ **Communicate, Communicate, Communicate:** Got a question? Stumped by a bug? Have a brilliant idea for a new feature? Don't be shy! Open an issue on GitHub, ask questions, and discuss your ideas *before* you dive into extensive coding. This saves everyone time and ensures we're all rowing in the same direction.
*   🤝 **Respect & Collaboration:** Treat everyone in the FMS community with respect and professionalism. We're all here to learn and build. Constructive feedback is gold; negativity is kryptonite.
*   ✨ **Quality Craftsmanship:** We take pride in writing code that is not just functional, but also clean, understandable, well-commented, and thoroughly tested. Think of yourself as an artisan crafting a fine piece of software.
*   🧩 **Incremental Victories:** Rome wasn't built in a day, and neither are complex features. Small, well-defined contributions (like a focused bug fix or a single, well-scoped feature enhancement) are often easier to review, test, and merge. This keeps the project moving forward smoothly.

## Getting Started: Your Contributor Launch Sequence 🚀

Ready to suit up? The setup for contributing is very similar to getting FMS running locally for development, with a couple of extra steps for smooth collaboration via GitHub.

**1. Your Developer Toolkit (Prerequisites):**

*   **Python:** Version 3.8 or higher (the language FMS speaks).
*   **pip:** Python's package installer (your tool for grabbing Python libraries).
*   **Git:** The version control system that lets us track changes and collaborate (your coding time machine!).
*   **A GitHub Account:** Your passport to the world of collaborative coding.
*   **(Potentially for Advanced Features/Testing):** While FMS defaults to SQLite for easy local development, the original `CONTRIBUTING.md` mentioned **PostgreSQL 12+** and **Redis**. These might be relevant if you're working on features that specifically need them or if you want to test in an environment closer to a potential production setup. *For most contributions, SQLite will be perfectly fine.*

**2. Fork It! (Create Your Own FMS Playground):**

*   Head over to the main FMS repository on GitHub: [https://github.com/Edmon02/faculty-management-system](https://github.com/Edmon02/faculty-management-system)
*   In the top-right corner, click the **"Fork"** button. This creates your personal copy (a "fork") of the FMS repository under your GitHub account. It's your own sandbox where you can experiment without affecting the original project.

**3. Clone Your Fork (Bring the Code Home):**

Now, download your forked repository to your local computer:
```bash
git clone https://github.com/YOUR_USERNAME/faculty-management-system.git
cd faculty-management-system
```
Don't forget to replace `YOUR_USERNAME` with your actual GitHub username!

**4. Connect to the Mothership (Set Upstream Remote):**

To keep your fork updated with the latest changes from the original (often called "upstream") FMS repository, you need to tell Git where it is:
```bash
git remote add upstream https://github.com/Edmon02/faculty-management-system.git
```
You can check your remotes with `git remote -v`. You should see both `origin` (your fork) and `upstream` (the original repo).

**5. Bubble Time! (Virtual Environment & Dependencies):**

As detailed in the [Getting Started Guide](./01_getting_started.md#2-create-and-activate-a-virtual-environment), create and activate a Python virtual environment. This keeps FMS's software needs tidy and separate. Then, install the necessary Python packages:
```bash
pip install -r requirements.txt
```
If there's a `requirements-dev.txt` or similar for development-specific tools (like testing frameworks), install that too:
```bash
# Example: if requirements-dev.txt exists
# pip install -r requirements-dev.txt
# For FMS, you might need to explicitly install testing tools if not in the main requirements:
pip install pytest pytest-flask flake8 pytest-cov
```

**6. Configure Your Local Universe (.env File):**

Set up your local environment variables using a `.env` file as described in the [Getting Started Guide](./01_getting_started.md#4-environment-configuration-env-file). This is especially important for setting a stable `SECRET_KEY` for development.

**7. Ignite the Engines! (Run Development Server):**
```bash
python run.py
```
You should now have FMS running locally, ready for your contributions!

## The Contribution Workflow: From Idea to Merged Reality ✨

Here's the typical journey your brilliant contribution will take:

**1. Branching: Your Creative Workspace:**

We (conceptually) follow a popular branching model similar to Gitflow. This keeps our codebase organized.

*   🌳 **`main` Branch:** This branch is sacred! It should always reflect the latest stable, production-ready code. Direct commits to `main` are usually a no-no.
*   🌿 **`develop` Branch:** This is the primary integration branch. All new features and bug fixes are developed in separate branches and then merged into `develop`. It's the "next version" in progress.
*   **✨ Feature Branches (`feature/<your-feature-name>`):** When you start working on a new feature, create a new branch *from the latest `develop` branch*.
    *   *Example:* `git checkout develop && git pull upstream develop && git checkout -b feature/advanced-reporting-module`
*   **🐛 Bugfix Branches (`fix/<bug-description>`):** For fixing those pesky bugs! Also branched from `develop` (or `main` for critical hotfixes, though that's less common for this project type).
    *   *Example:* `git checkout develop && git pull upstream develop && git checkout -b fix/user-login-redirect-loop`
*   **📜 Documentation Branches (`docs/<topic-of-docs>`):** If you're solely improving the documentation.
    *   *Example:* `git checkout develop && git pull upstream develop && git checkout -b docs/clarify-deployment-steps`

**2. The Creative Process (Making Changes):**

*   **Code with Passion:** Implement your feature or squash that bug on your dedicated branch.
*   **Adhere to Standards:** Follow the [Code Standards](#code-standards-writing-fms-style-code) outlined below. Clean, consistent code is happy code!
*   **Test, Test, Test!:**
    *   For **new features**, write new automated tests (using Pytest) that thoroughly cover the functionality you've added.
    *   For **bug fixes**, write a test that *specifically reproduces the bug* (it should fail before your fix) and then *passes after your fix is applied*. This ensures the bug stays squashed!
    *   Aim for the project's target of **80%+ test coverage** for any new code you introduce.
*   **Document Your Deeds:** If your changes impact how users interact with FMS, how it's configured, or its architecture, please update the relevant sections in our `/docs` directory. Good documentation is a gift to your future self and other developers!

**3. Commit Like a Pro (Meaningful Commit Messages):**

Clear commit messages are like well-written chapter titles – they make the project's history easy to read and understand. We strive to follow the [**Conventional Commits**](https://www.conventionalcommits.org/en/v1.0.0/) specification.

**The Golden Format:**
```
<type>(<optional_scope>): <short_description>

[optional_body_providing_more_detail]

[optional_footer(s)_like_Closes_#123_or_BREAKING_CHANGE]
```

**Common Commit Types (Your Commit Verbs!):**

*   `feat`: You've added a cool new feature! (e.g., `feat(student): implement course enrollment via API`)
*   `fix`: You've squashed a bug! (e.g., `fix(auth): correct redirect loop after password reset`)
*   `docs`: You've improved the documentation! (e.g., `docs(readme): add badges and update setup instructions`)
*   `style`: Code style changes that don't affect logic (e.g., `style(user_model): apply black formatting`)
*   `refactor`: You've restructured code without changing its behavior (e.g., `refactor(service): extract email sending to utility function`)
*   `perf`: You've made the code run faster! (e.g., `perf(db_query): optimize student list fetching with index`)
*   `test`: You've added or improved tests! (e.g., `test(payment): add unit tests for Stripe integration`)
*   `chore`: Routine maintenance, build process changes, etc. (e.g., `chore: update flask dependency to 2.3.0`)

**Example of a Great Commit Message:**
```
feat(exercise): allow file attachments for exercise submissions

Students can now upload files (PDF, DOCX, TXT) when submitting
an exercise. This change modifies the `SubmittedExercise` model
and updates the submission form in the student dashboard.

- Adds `attached_filename` and `attached_file_path` to `SubmittedExercise` model.
- Updates `submit_exercise_form` to include a file input.
- Modifies `ExerciseService` to handle file uploads securely.

Closes #42
```

**4. Stay in Sync (Keep Your Branch Updated):**

Before you're ready to propose your changes (i.e., before creating a Pull Request), make sure your feature branch has all the latest updates from the main `develop` branch of the *upstream* (original) repository. This is best done using `rebase`:

```bash
# Make sure you've committed all your local changes on your feature branch first!
git checkout your-feature-branch

# Fetch the latest changes from the upstream remote (the original FMS repo)
git fetch upstream

# Rebase your feature branch on top of the latest upstream/develop
git rebase upstream/develop
```
You might encounter "merge conflicts" if changes in `develop` overlap with yours. Git will guide you through resolving them. Rebasing keeps the project history cleaner and more linear.

**5. The Grand Proposal: Your Pull Request (PR) 💌**

This is where you formally propose merging your changes into the FMS project.

*   **Push to Your Fork:** Send your committed changes from your local feature branch to your fork on GitHub:
    ```bash
    git push origin your-feature-branch
    ```
*   **Create the PR:** Go to your FMS fork on GitHub. You should see a prominent button or banner suggesting you create a Pull Request from `your-feature-branch` to the `Edmon02/faculty-management-system` repository's `develop` branch. Click it!
*   **The PR Perfection Checklist:**
    *   **Compelling Title:** Make it clear and concise. Following the Conventional Commits format here is also great (e.g., `feat(student): Add bulk student import via CSV`).
    *   **Detailed Description:** This is your chance to shine!
        *   Clearly explain **what** your changes do and **why** you made them.
        *   If it fixes an existing GitHub Issue, link to it (e.g., "Closes #42", "Addresses #101").
        *   **Show, Don't Just Tell:** For UI changes, include screenshots or even short GIFs! They are worth a thousand words.
    *   **Self-Review:** Read through your own changes one last time (the "Files changed" tab in the PR).
    *   **Tests Passing?** Confirm that all automated tests (`pytest`) pass with your changes. Run them locally before pushing if you haven't recently.
    *   **Linter Happy?** Ensure your code is clean according to `flake8` (`flake8 app/ tests/ run.py`).
    *   **Docs Updated?** If your changes require it, confirm you've updated the documentation in the `/docs` directory.
*   **The Review Process:** Once your PR is submitted, project maintainers will review your code. They might ask questions or suggest changes. This is a normal and healthy part of the collaborative process! Be responsive and open to feedback.

## Code Standards: Writing FMS-Style Code ✍️

Consistency is key to a maintainable and understandable codebase. Here are our style preferences:

**Python (Our Backend Language):**

*   **PEP 8 is King:** Please follow the [PEP 8 Style Guide for Python Code](https://pep8.org/). If you use an auto-formatter like [Black](https://github.com/psf/black) or [YAPF](https://github.com/google/yapf), configure it for PEP 8 compliance.
*   **Type Hints are Your Friends:** For all new functions and methods, please use Python type hints. They make code much easier to understand and help static analysis tools catch bugs early.
    ```python
    from typing import List, Optional
    from app.models.student import Student # Assuming your Student model

    def get_student_by_id(student_id: int) -> Optional[Student]:
        # Your amazing code here
        pass
    ```
*   **Docstrings: Explain Thyself!** Write clear, concise docstrings for all modules, classes, functions, and methods. We lean towards the [Google Python Style Guide for Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
    ```python
    def calculate_grade_average(scores: List[float], weights: Optional[List[float]] = None) -> float:
        """Calculates the (optionally weighted) average of a list of scores.

        If weights are provided, they must correspond to each score.
        If no weights are provided, a simple average is computed.

        Args:
            scores: A list of scores (float).
            weights: An optional list of weights (float) for each score.

        Returns:
            The calculated average, or 0.0 if scores list is empty.

        Raises:
            ValueError: If weights are provided but their count doesn't match scores.
        """
        if not scores:
            return 0.0
        # ... rest of your brilliant logic ...
    ```
*   **Import Order:** Keep your imports organized as per PEP 8:
    1.  Standard library imports (e.g., `import os`, `from datetime import datetime`)
    2.  Third-party library imports (e.g., `from flask import Blueprint`, `import sqlalchemy`)
    3.  Local application/library specific imports (e.g., `from app.models import User`, `from app.services.auth_service import AuthService`)
    *Separate each group with a blank line.*
*   **Flask-Specific Wisdom:**
    *   **Blueprints for Organization:** Structure your routes using Flask Blueprints (see `app/routes/`).
    *   **Service Layer for Logic:** Keep your business logic in the service layer (`app/services/`). This keeps your route functions (controllers) thin and focused on request/response handling.
    *   **SQLAlchemy for Data:** Use SQLAlchemy models (`app/models/`) for all database interactions.
    *   **Authentication:** The FMS currently uses session-based authentication. If you're working on auth-related features, maintain consistency with this pattern. (The original `CONTRIBUTING.md` mentioned JWT; if that's a future direction, it would be a larger discussion).

**HTML (Our Jinja2 Templates):**

*   **Build on `base.html`:** All main application pages should `{% extends "base.html" %}`.
*   **Don't Repeat Yourself (DRY) with Includes/Macros:** For common UI elements (like page headers, search forms, and especially form fields), use the existing includes and macros in `app/templates/includes/`. The `render_form_field` macro in `_forms.html` is your best friend for forms!
*   **`url_for()` is Your Navigator:** *Always* use `url_for('blueprint_name.route_function_name', ...)` to generate URLs for internal links and form actions. Hardcoding URLs like `/students/add` is fragile and will break if routes change.
*   **Think Accessibility (A11y):** Strive for accessible HTML. Use `<label>` for form inputs, provide `alt` text for images if they convey meaning, use semantic HTML5 elements where appropriate.
*   **Keep it Tidy:** Readable, well-indented templates make everyone happier.

**JavaScript (For Frontend Interactions & Embedded Magic):**

*   **Clarity is Queen:** Write JavaScript that is easy to understand. Comment any complex logic or tricky parts.
*   **Handle Errors Gracefully:** Especially for AJAX requests, make sure you handle potential errors and provide feedback to the user.
*   **Security Awareness:** If you're manipulating the DOM with data that might have come from user input, be mindful of Cross-Site Scripting (XSS) risks. (Though server-side rendering with Jinja2's auto-escaping provides a good layer of protection for data passed from the backend).
*   **Follow Existing Patterns:** Look at how JavaScript is used elsewhere in the project (e.g., in `exercises.html` or `waitingroom.html` after refactoring) for consistency.

**Testing (Our Quality Guarantee):**

*   **Pytest is Our Tool:** Write your backend tests using Pytest.
*   **Aim for Coverage:** The project aims for 80%+ test coverage for new code. Use `pytest-cov` to check your coverage.
*   **Factory Boy (If in Use):** The original `CONTRIBUTING.md` mentioned Factory Boy. If it's being used in the project for generating test data, familiarize yourself with its patterns.

## Tutorial: Adding a New Feature (Example: "Subject Office Hours")

Let's imagine you want to add a feature where lecturers can specify "Office Hours" for each subject they teach.

**1. Understand & Discuss the Requirement:**
   *   **Goal:** Lecturers can input a text string (e.g., "Mon 10-12, Wed 2-3 via Zoom (link)") for each subject's office hours. Students can view these.
   *   **Discussion (Open an Issue!):** "I'd like to add an 'Office Hours' field to subjects. Thinking of a text field in the Subject model and updating the add/edit subject forms. Students would see this on the subject list/details page. Thoughts?"

**2. Plan Your Attack:**
   *   **Model (`app/models/subject.py`):** Add a new `office_hours = db.Column(db.String(255), nullable=True)` field to the `Subject` model.
   *   **Service (`app/services/subject_service.py`):** Ensure `create` and `update` methods for subjects can handle the new `office_hours` data.
   *   **Controller & Routes (`app/controllers/subject_controller.py`, `app/routes/subjects.py`):** Modify `addSubject` and `editSubject` to pass `office_hours` data from the form to the service.
   *   **Templates:**
        *   `app/templates/subjects/add-subject.html` & `edit-subject.html`: Add a new form field (using our `render_form_field` macro!) for "Office Hours."
        *   `app/templates/subjects/subjects.html`: Display the office hours in the subject cards.
   *   **Tests:** Add tests for the new model field and ensure office hours can be set and displayed.

**3. Create Your Feature Branch:**
   ```bash
   git checkout develop
   git pull upstream develop # Get the latest from the main project
   git checkout -b feature/subject-office-hours
   ```

**4. Implement Model Changes:**
   Open `app/models/subject.py` and add the new field to the `Subject` class:
   ```python
   class Subject(db.Model):
       # ... existing fields ...
       office_hours = db.Column(db.String(255), nullable=True) # New field!
       # ...
   ```
   *(If using database migrations like Alembic, you'd generate a new migration script here. For `db.create_all()` used in dev, it might pick up the new column if the DB is recreated).*

**5. Implement Service & Controller Changes:**
   *   Modify methods in `SubjectService` to accept and save `office_hours`.
   *   Update `SubjectController` to pass `office_hours` from `request.form` to the service.

**6. Implement Template Changes:**
   *   In `add-subject.html` and `edit-subject.html` (inside the form):
     ```html+jinja
     {# Import the macro at the top of the file if not already there #}
     {% from "includes/_forms.html" import render_form_field %}

     {{ render_form_field(name='office_hours', label='Office Hours', field_type='textarea', value=subject.office_hours if subject else '', placeholder='e.g., Mon 10-12, Wed 2-3 via Zoom (link)', col_class='col-12') }}
     ```
   *   In `subjects.html` (inside the `subj-card` loop):
     ```html+jinja
     {% if subject_item.office_hours %}
         <p class="card-text"><small class="text-muted"><strong>Office Hours:</strong> {{ subject_item.office_hours }}</small></p>
     {% endif %}
     ```

**7. Write Your Tests:**
   *   In `tests/test_models.py`, add a test to ensure a `Subject` can be created with office hours.
   *   In `tests/test_routes.py`, update tests for adding/editing subjects to include the `office_hours` field. Add an assertion to check if office hours are displayed on the subjects page.

**8. Document Your Feature:**
   *   Update `docs/04_features.md` to mention the new "Office Hours" capability under "Subject Management."
   *   If it's a significant architectural change (not in this case), `docs/02_architecture.md` might need a touch.

**9. Commit, Rebase, Push, and Create Your PR:**
   Follow the workflow: write good commit messages, rebase on `upstream/develop`, push to your fork, and create a detailed Pull Request.

This example gives you a practical feel for the contribution lifecycle.

## Reporting Issues & Bug Reports: Help Us Improve! 🐞

Found a glitch? Something behaving unexpectedly? Your bug reports are invaluable!

1.  **Check Existing Issues First:** Before reporting, quickly search the GitHub Issues for FMS to see if someone has already reported the same problem.
2.  **If It's New, Provide the Deets:** Create a new issue on GitHub with as much information as possible:
    *   **Title:** Clear and descriptive (e.g., "Login button unresponsive on Firefox after password error").
    *   **What I Expected:** Briefly describe what you thought should happen.
    *   **What Actually Happened:** Describe the bug.
    *   **Steps to Reproduce (Super Important!):** Provide clear, step-by-step instructions so others can reliably reproduce the issue. This is the #1 thing that helps us fix bugs fast!
    *   **Your Setup (Environment Details):**
        *   Your Operating System (e.g., Windows 10, macOS Ventura, Ubuntu 22.04).
        *   Python version (e.g., `python --version`).
        *   Browser and version (e.g., Chrome 105, Firefox 103).
        *   FMS version or Git commit hash, if you know it.
    *   **Evidence (Logs/Screenshots):**
        *   Include any error messages from your browser's developer console (usually F12).
        *   Include relevant error messages or tracebacks from the Flask server logs (your terminal).
        *   Screenshots or short videos illustrating the problem are often incredibly helpful!

---

**Thank you for considering contributing to the Faculty Management System!** Every contribution, big or small, helps us build a better tool for educators and students. We look forward to your ideas and your code!
