import pytest

from app.models.lecturer import Lecturer
from app.models.student import Student
from app.models.user import User


def test_user_model():
    # Test user creation
    user = User(username="testuser", password="password123", _id=1, type="student")

    assert user.username == "testuser"
    assert user.password == "password123"
    assert user._id == 1
    assert user.type == "student"


def test_student_model():
    # Test student creation
    student = Student(id=1, first_name="John", last_name="Doe", patronymic="Smith", birthday_date="2000-01-01", phone="1234567890", group_name="Group A", image=b"", rating=0)

    assert student.id == 1
    assert student.first_name == "John"
    assert student.last_name == "Doe"
    assert student.patronymic == "Smith"
    assert student.birthday_date == "2000-01-01"
    assert student.phone == "1234567890"
    assert student.group_name == "Group A"
    assert student.image == b""
    assert student.rating == 0


def test_lecturer_model():
    # Test lecturer creation
    lecturer = Lecturer(
        id=1, first_name="Jane", last_name="Smith", patronymic="Doe", position="Professor", academic_degree="PhD", email="jane@example.com", phone="0987654321", images=b"", is_Admin=0, is_Lecturer=1
    )

    assert lecturer.id == 1
    assert lecturer.first_name == "Jane"
    assert lecturer.last_name == "Smith"
    assert lecturer.patronymic == "Doe"
    assert lecturer.position == "Professor"
    assert lecturer.academic_degree == "PhD"
    assert lecturer.email == "jane@example.com"
    assert lecturer.phone == "0987654321"
    assert lecturer.images == b""
    assert lecturer.is_Admin == 0
    assert lecturer.is_Lecturer == 1
