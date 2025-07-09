# Changelog: The Evolving Story of FMS 📜

Welcome to the official changelog for the **Faculty Management System (FMS)**! This document is where we meticulously record all notable changes, enhancements, bug fixes, and epic new features that get added to the project.

We follow the principles outlined at [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and strive to adhere to [Semantic Versioning (SemVer)](https://semver.org/spec/v2.0.0.html) for our releases. This means you can easily track how the project grows and understand the impact of different versions.

---

## [Unreleased] - What We're Cooking Up! 🍳🔥

This section details changes that have been merged into our development branch but haven't yet been packaged into an official release.

### Added ✨
*(New features and significant enhancements)*
*   `[Feature]` New student dashboard UI components: We're giving the student dashboard a fresh coat of paint and some new widgets for an even better user experience!
*   `[API]` Endpoint for bulk exercise submissions: Introducing a new API endpoint to allow for programmatic submission of exercises in bulk – power-user stuff!
*   `[Docs]` **Comprehensive Documentation Initiative (Ongoing):**
    *   Established a full documentation structure within the `/docs` directory.
    *   Created initial detailed content for all key sections: Overview, Getting Started, Architecture, Code Walkthrough, Features, Configuration, Testing, Deployment, Contributing, FAQ & Glossary, and this Changelog.
    *   Began a refinement pass to enhance engagement, add narrative, examples, and ensure clarity across all documentation.
*   `[Refactor]` **HTML Template Overhaul for Clarity & Maintainability:**
    *   Introduced Jinja2 includes (`_page_header.html`, `_search_form.html`) for common UI patterns, reducing code duplication.
    *   Developed a powerful Jinja2 macro (`render_form_field` in `_forms.html`) to standardize and simplify the creation of form fields across various add/edit pages.
    *   Refactored key list-based templates (students, teachers, exercises) and form-based templates (add/edit students, add exercise, subjects, news, waitingroom) to utilize these new includes and macros, resulting in cleaner and more consistent template code.

### Changed 🔄
*(Modifications to existing functionality)*
*   `[Refactor]` Authentication service now uses JWT claims for enhanced session management and security. (This was a previous item, kept for historical context if it was recent).
*   `[Perf]` Optimized database queries within the `StudentService` for faster retrieval of student lists, especially with filters. (Previous item).
*   `[Refactor]` **`base.html` Enhancements:**
    *   Cleaned up and organized CSS and JavaScript links.
    *   Removed duplicate script inclusions.
    *   Moved page-specific JavaScript from `base.html` into the relevant child templates' `{% block scripts %}` or dedicated static JS files.
    *   Ensured consistent use of `url_for()` for internal links, replacing hardcoded paths.
*   `[Docs]` Enhanced all existing documentation files (`00_overview.md` through `09_faq_glossary.md`, and this `CHANGELOG.md`) with more engaging narrative, analogies, examples, and detailed explanations as part of the "Refine Documentation" pass.

### Fixed 🐞
*(Bug fixes that make FMS more reliable)*
*   `[Security]` Patched a potential Cross-Site Scripting (XSS) vulnerability found in the news comments display. (Previous item).
*   `[Bug]` Resolved an issue where file uploads larger than 2MB were incorrectly failing, even if `MAX_CONTENT_LENGTH` was set higher. (Previous item).

### Removed 🗑️
*(Features or code that have been removed)*
*   *(Nothing removed in this recent pass yet)*

---

## [1.0.0] - 2023-11-15 - Our Grand Debut! 🎉

### Initial Release

This was the first official version of the Faculty Management System, bringing forth the core functionalities that set the stage for future awesomeness!

*   Core university management features established.
*   Functional student and lecturer portals with role-based access.
*   Basic exercise submission and tracking system implemented.
*   News and announcement system for departmental communication.

---

*This changelog is a living document. We'll keep it updated as FMS continues to evolve and improve!*
