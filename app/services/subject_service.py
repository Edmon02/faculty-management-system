# app/services/subject_service.py
from typing import Dict, List, Optional

from app.models.files import FileModel
from app.models.subject import Subject, SubjectFile, SubjectLecturerGroup


class SubjectService:
    @staticmethod
    def get_subjects_by_groups(group_ids: List[str]) -> List[Dict]:
        """
        Get all subjects for the specified groups.

        Args:
            group_ids: List of group IDs

        Returns:
            List of subject data dictionaries
        """
        subjects = Subject.query.join(SubjectLecturerGroup, Subject.id == SubjectLecturerGroup.subject_id).filter(SubjectLecturerGroup.group_name.in_(group_ids)).distinct().all()

        result = []
        for subject in subjects:
            subject_dict = subject.to_dict()

            # Get files for this subject
            files = FileModel.query.join(SubjectFile, FileModel.id == SubjectFile.file_id).filter(SubjectFile.subject_id == subject.id).all()

            file_list = []
            for file in files:
                file_list.append({"file_name": file.file_name, "file_type": file.file_name.split(".")[-1] if "." in file.file_name else "", "file_id": file.id})

            subject_dict["files"] = file_list
            result.append(subject_dict)

        return result

    @staticmethod
    def add_file_to_subject(subject_id: int, file_name: str, file_data: bytes) -> bool:
        """
        Add a file to a subject.

        Args:
            subject_id: The subject ID
            file_name: The name of the file
            file_data: The file content as bytes

        Returns:
            True if successful, False otherwise
        """
        # Check if the file already exists
        existing_file = FileModel.query.filter_by(file_name=file_name).first()

        if existing_file:
            file_id = existing_file.id
        else:
            # Create a new file record
            new_file = FileModel(file=file_data, file_name=file_name)
            new_file.save()
            file_id = new_file.id

        # Check if the subject-file connection already exists
        existing_connection = SubjectFile.query.filter_by(subject_id=subject_id, file_id=file_id).first()

        if not existing_connection:
            # Create the connection
            new_connection = SubjectFile(subject_id=subject_id, file_id=file_id)
            new_connection.save()

        return True
