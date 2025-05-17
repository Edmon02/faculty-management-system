# app/services/student_service.py
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd

from app.models.student import Student
from app.models.user import User
from app.services.auth_service import AuthService


class StudentService:
    @staticmethod
    def get_students_by_groups(group_ids: List[str]) -> List[Dict]:
        """
        Get all students in the specified groups.

        Args:
            group_ids: List of group IDs

        Returns:
            List of student data dictionaries
        """
        students = Student.query.filter(Student.group_name.in_(group_ids)).all()
        return [student.to_dict() for student in students]

    @staticmethod
    def get_student_by_id(student_id: int) -> Optional[Dict]:
        """
        Get a student by ID.

        Args:
            student_id: The student ID

        Returns:
            Student data dictionary or None if not found
        """
        student = Student.query.filter_by(id=student_id).first()
        return student.to_dict() if student else None

    @staticmethod
    def create_student(data: Dict) -> int:
        """
        Create a new student and associated user.

        Args:
            data: Dictionary containing student data

        Returns:
            ID of the newly created student
        """
        # Process date if it's a string
        if isinstance(data.get("birthday_date"), str):
            data["birthday_date"] = datetime.strptime(data["birthday_date"], "%Y-%m-%d")

        # Create the student
        student = Student(
            group_name=data.get("group_name"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            patronymic=data.get("patronymic"),
            birthday_date=data.get("birthday_date"),
            phone=data.get("phone"),
            image=data.get("image", b""),
        )
        student.save()

        # Create associated user
        username = AuthService.random_numbers(8)
        password = AuthService.random_password(10)
        hashed_password = AuthService.hash_password(password)

        user = User(username=username, password=hashed_password, _id=student.id, type="student")
        user.save()

        return student.id

    @staticmethod
    def update_student(student_id: int, data: Dict) -> bool:
        """
        Update an existing student.

        Args:
            student_id: The ID of the student to update
            data: Dictionary containing updated student data

        Returns:
            True if successful, False otherwise
        """
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return False

        # Process date if it's a string
        if isinstance(data.get("birthday_date"), str):
            data["birthday_date"] = datetime.strptime(data["birthday_date"], "%Y-%m-%d")

        # Update fields
        if "group_name" in data:
            student.group_name = data["group_name"]
        if "first_name" in data:
            student.first_name = data["first_name"]
        if "last_name" in data:
            student.last_name = data["last_name"]
        if "patronymic" in data:
            student.patronymic = data["patronymic"]
        if "birthday_date" in data:
            student.birthday_date = data["birthday_date"]
        if "phone" in data:
            student.phone = data["phone"]
        if "image" in data and data["image"]:
            student.image = data["image"]

        student.save()
        return True

    @staticmethod
    def import_students_from_excel(file_path: str) -> List[int]:
        """
        Import students from Excel file.

        Args:
            file_path: Path to the Excel file

        Returns:
            List of IDs of the newly created students
        """
        df = pd.read_excel(file_path)
        student_ids = []

        for _, row in df.iterrows():
            student_data = {
                "first_name": row["Name"],
                "last_name": row["Surname"],
                "patronymic": row["Patronymic"],
                "phone": row["Phone"],
                "birthday_date": row["Birthday"],
                "group_name": row["Group"],
            }

            student_id = StudentService.create_student(student_data)
            student_ids.append(student_id)

        return student_ids
