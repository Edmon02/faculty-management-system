# Contribution Guidelines

Thank you for considering contributing to the University Education Platform!  
Please take a moment to review these guidelines before submitting changes.

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL 12+ (or your preferred DBMS)
- Redis (for caching/queues)
- Git

### Setup
1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
4. Set up environment variables (copy `.env.example` to `.env`)
5. Run the development server:
   ```bash
   flask run --debug
   ```

## Workflow

### Branching Strategy
- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation changes

### Commit Message Convention
Follow [Conventional Commits](https://www.conventionalcommits.org):
```
<type>(<scope>): <subject>

<body>

<footer>
```

Common types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test additions
- `chore`: Maintenance tasks

### Pull Requests
1. Create a feature branch from `develop`
2. Ensure all tests pass (`pytest`)
3. Update documentation if needed
4. Open PR with:
   - Clear description of changes
   - Screenshots for UI changes
   - Reference to related issues

## Code Standards

### Python
- Follow [PEP 8](https://pep8.org)
- Type hints for all new code
- Docstrings following [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

### Flask Specifics
- Blueprints for route organization
- Services layer for business logic
- SQLAlchemy for database operations
- JWT for authentication

### Testing
- Pytest for unit/integration tests
- 80%+ test coverage expected
- Factory Boy for test data

## Reporting Issues
Include:
1. Expected vs actual behavior
2. Steps to reproduce
3. Environment details
4. Relevant logs/screenshots