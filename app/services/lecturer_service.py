# app/services/lecturer_service.py
from typing import Dict, List, Optional

from app.models.lecturer import Lecturer
from app.models.subject import Subject, SubjectLecturerGroup


class LecturerService:
    @staticmethod
    def get_lecturers_by_groups(group_ids: List[str]) -> List[Dict]:
        """
        Get all lecturers teaching the specified groups.

        Args:
            group_ids: List of group IDs

        Returns:
            List of lecturer data with subject and group information
        """
        result = []

        # Use a join to get lecturers with their subjects and groups
        lecturers_data = (
            Lecturer.query.join(SubjectLecturerGroup, Lecturer.id == SubjectLecturerGroup.lecturer_id)
            .join(Subject, SubjectLecturerGroup.subject_id == Subject.id)
            .filter(SubjectLecturerGroup.group_name.in_(group_ids))
            .with_entities(
                Lecturer.id,
                Lecturer.first_name,
                Lecturer.last_name,
                Lecturer.academic_degree,
                Lecturer.position,
                Lecturer.email,
                Lecturer.images,
                Lecturer.is_Admin,
                Lecturer.is_Lecturer,
                Subject.subject_name,
                SubjectLecturerGroup.group_name,
            )
            .all()
        )

        # Convert to dictionaries
        for data in lecturers_data:
            lecturer_dict = {
                "id": data[0],
                "first_name": data[1],
                "last_name": data[2],
                "academic_degree": data[3],
                "position": data[4],
                "email": data[5],
                "images": data[6],
                "is_Admin": data[7],
                "is_Lecturer": data[8],
                "subject_name": data[9],
                "group_name": data[10],
            }
            result.append(lecturer_dict)

        return result

    @staticmethod
    def get_lecturer_by_id(lecturer_id: int) -> Optional[Dict]:
        """
        Get a lecturer by ID.

        Args:
            lecturer_id: The lecturer ID

        Returns:
            Lecturer data dictionary or None if not found
        """
        lecturer = Lecturer.query.filter_by(id=lecturer_id).first()
        return lecturer.to_dict() if lecturer else None

    @staticmethod
    def update_lecturer(lecturer_id: int, data: Dict) -> bool:
        """
        Update an existing lecturer.

        Args:
            lecturer_id: The ID of the lecturer to update
            data: Dictionary containing updated lecturer data

        Returns:
            True if successful, False otherwise
        """
        lecturer = Lecturer.query.filter_by(id=lecturer_id).first()
        if not lecturer:
            return False

        # Update fields
        if "first_name" in data:
            lecturer.first_name = data["first_name"]
        if "last_name" in data:
            lecturer.last_name = data["last_name"]
        if "academic_degree" in data:
            lecturer.academic_degree = data["academic_degree"]
        if "position" in data:
            lecturer.position = data["position"]
        if "email" in data:
            lecturer.email = data["email"]
        if "images" in data and data["images"]:
            lecturer.images = data["images"]
        if "is_Admin" in data:
            lecturer.is_Admin = data["is_Admin"]
        if "is_Lecturer" in data:
            lecturer.is_Lecturer = data["is_Lecturer"]

        lecturer.save()
        return True
