# Faculty Management System

  

A comprehensive web application for managing faculty information, including students, teachers, courses, and more.

  

## Project Structure

  

The project follows a modular Flask application structure:

```
faculty-management-system/

├── app/

│ ├── __init__.py # Application factory

│ ├── config.py # Configuration settings

│ ├── models/ # Database models

│ ├── routes/ # Route definitions

│ ├── services/ # Business logic

│ ├── controllers/ # Request/response handling

│ ├── static/ # Static assets

│ ├── templates/ # HTML templates

│ ├── utils/ # Utility functions

│ └── extensions.py # Flask extensions initialization

├── migrations/ # Database migrations

├── tests/ # Test files

├── .env # Environment variables

├── .env.example # Example environment variables

├── .gitignore # Git ignore file

├── requirements.txt # Project dependencies

├── run.py # Application entry point

└── README.md # Project documentation
```
  

## Features

  

- User authentication and role-based access control

- Student management

- Teacher management

- Course/Subject management

- Exercise assignments

- News publication

- Activity tracking and reporting

- File uploads and downloads

- Chatbot integration

  

## Getting Started

  

### Prerequisites

  

- Python 3.8 or higher

- SQLite

  

### Installation

  

1. Clone the repository:

```

git clone https://github.com/Edmon02/faculty-management-system.git

cd faculty-management-system

```

  

2. Create a virtual environment and activate it:

```

python -m venv venv

source venv/bin/activate # On Windows: venv\Scripts\activate

```

  

3. Install the dependencies:

```

pip install -r requirements.txt

```

  

4. Create a `.env` file based on `.env.example`:

```

cp .env.example .env

```

  

5. Run the application:

```

flask run

```

Or use the run script:

```

python run.py

```

  

## Development

  

### Database Setup

  

The application uses SQLite as its database. The database file is created automatically when the application is run for the first time.

  

### Testing

  

Run tests with pytest:

```

pytest

```

  

### Code Quality

  

Ensure your code adheres to PEP 8 standards by running flake8:

```

flake8

```

  

## Default User Accounts

  

For testing purposes, the following accounts are available:

  

- Admin:

- Username: fYRKVPTdzT

- Password: 03611557

  

- Lecturer:

- Username: fYRKVPTdzm

- Password: 71319352

  

- Student:

- Username: ElwAiWgAZg

- Password: 03611558

  

## License

  

This project is licensed under the MIT License - see the LICENSE file for details.

```

  

# requirements.txt

```

flask==2.2.3

flask-cors==3.0.10

flask-limiter==3.3.1

flask-wtf==1.1.1

pandas==2.0.0

bokeh==3.1.0

openpyxl==3.1.2

pydub==0.25.1

scikit-learn==1.2.2

nltk==3.8.1

python-dotenv==1.0.0

waitress==2.1.2

```
