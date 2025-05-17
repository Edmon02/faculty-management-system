-- Test data for the database

-- Create tables
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    _id INTEGER NOT NULL,
    type TEXT NOT NULL,
    failed_attempts INTEGER DEFAULT 0,
    last_failed_attempt TEXT
);

CREATE TABLE IF NOT EXISTS Student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    patronymic TEXT,
    birthday_date TEXT,
    phone TEXT,
    group_name TEXT,
    image BLOB,
    rating INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Lecturer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    patronymic TEXT,
    position TEXT,
    academic_degree TEXT,
    email TEXT,
    phone TEXT,
    images BLOB,
    is_Admin INTEGER DEFAULT 0,
    is_Lecturer INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Subject (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT NOT NULL,
    group_name TEXT,
    messenge TEXT
);

CREATE TABLE IF NOT EXISTS Files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file BLOB,
    file_name TEXT
);

CREATE TABLE IF NOT EXISTS SubjectFile (
    subject_id INTEGER,
    file_id INTEGER,
    PRIMARY KEY (subject_id, file_id),
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id),
    FOREIGN KEY (file_id) REFERENCES Files(id)
);

CREATE TABLE IF NOT EXISTS News (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    title TEXT,
    date TEXT,
    cover BLOB,
    desc TEXT,
    audio BLOB
);

-- Insert test data
INSERT INTO Users (username, password, _id, type) VALUES 
('test', 'test', 1, 'student'),
('admin', 'admin', 1, 'admin'),
('lecturer', 'lecturer', 1, 'lecturer');

INSERT INTO Student (first_name, last_name, patronymic, birthday_date, phone, group_name) VALUES 
('John', 'Doe', 'Smith', '2000-01-01', '1234567890', 'Group A');

INSERT INTO Lecturer (first_name, last_name, patronymic, position, academic_degree, email, phone, is_Admin, is_Lecturer) VALUES 
('Jane', 'Smith', 'Doe', 'Professor', 'PhD', 'jane@example.com', '0987654321', 1, 1);

INSERT INTO Subject (subject_name, group_name) VALUES 
('Mathematics', 'Group A'),
('Physics', 'Group A'),
('Computer Science', 'Group A');

INSERT INTO News (category, title, date, desc) VALUES 
('Department', 'Welcome to the new academic year', '2023-09-01', 'We are excited to welcome all students to the new academic year!');