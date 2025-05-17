# app/services/exercise_service.py
from datetime import datetime
from typing import Dict, List, Optional

from app.models.exercise import Exercise, ExerciseGroup, WaitRoom
from app.models.student import Student


class ExerciseService:
    @staticmethod
    def get_exercises_by_groups(group_ids: List[str], student_id: Optional[int] = None) -> List[Dict]:
        """
        Get all exercises for the specified groups.

        Args:
            group_ids: List of group IDs
            student_id: Optional student ID to check wait room status

        Returns:
            List of exercise data dictionaries
        """
        exercises = Exercise.query.join(ExerciseGroup, Exercise.id == ExerciseGroup.exercise_id).filter(ExerciseGroup.group_name.in_(group_ids)).all()

        result = []
        for exercise in exercises:
            exercise_dict = exercise.to_dict()

            # Check if the student has this exercise in wait room
            if student_id:
                wait_entry = WaitRoom.query.filter_by(student_id=student_id, exercise_id=exercise.id).first()
                exercise_dict["checkType"] = 1 if wait_entry else 0
            else:
                exercise_dict["checkType"] = 0

            # Add file extension
            if exercise.file_name:
                exercise_dict["file_type"] = exercise.file_name.split(".")[-1] if "." in exercise.file_name else ""

            result.append(exercise_dict)

        return result

    @staticmethod
    def create_exercise(data: Dict) -> int:
        """
        Create a new exercise.

        Args:
            data: Dictionary containing exercise data

        Returns:
            ID of the newly created exercise
        """
        exercise = Exercise(expiry_time=data.get("expiry_time"), messenge=data.get("messenge"), subject_name=data.get("subject_name"), file_name=data.get("file_name"))
        exercise.save()

        # Create group association
        if "group_name" in data:
            group = ExerciseGroup(exercise_id=exercise.id, group_name=data.get("group_name"))
            group.save()

        return exercise.id

    @staticmethod
    def update_exercise(exercise_id: int, data: Dict) -> bool:
        """
        Update an existing exercise.

        Args:
            exercise_id: The ID of the exercise to update
            data: Dictionary containing updated exercise data

        Returns:
            True if successful, False otherwise
        """
        exercise = Exercise.query.filter_by(id=exercise_id).first()
        if not exercise:
            return False

        # Update fields
        if "expiry_time" in data:
            exercise.expiry_time = data["expiry_time"]
        if "messenge" in data:
            exercise.messenge = data["messenge"]
        if "subject_name" in data:
            exercise.subject_name = data["subject_name"]
        if "file_name" in data and data["file_name"]:
            exercise.file_name = data["file_name"]

        exercise.save()

        # Update group if provided
        if "group_name" in data:
            # Check if association exists
            group = ExerciseGroup.query.filter_by(exercise_id=exercise_id).first()
            if group:
                group.group_name = data["group_name"]
                group.save()
            else:
                new_group = ExerciseGroup(exercise_id=exercise_id, group_name=data["group_name"])
                new_group.save()

        return True

    @staticmethod
    def delete_exercise(exercise_id: int) -> bool:
        """
        Delete an exercise.

        Args:
            exercise_id: The ID of the exercise to delete

        Returns:
            True if successful, False otherwise
        """
        exercise = Exercise.query.filter_by(id=exercise_id).first()
        if not exercise:
            return False

        # Delete associated group entries
        ExerciseGroup.query.filter_by(exercise_id=exercise_id).delete()

        # Delete wait room entries
        WaitRoom.query.filter_by(exercise_id=exercise_id).delete()

        # Delete the exercise
        exercise.delete()
        return True

    @staticmethod
    def get_waiting_room_data() -> Dict:
        """
        Get data for the waiting room.

        Returns:
            Dictionary containing waiting room data
        """
        # Get all entries in the wait room with their related data
        results = (
            WaitRoom.query.join(Exercise, WaitRoom.exercise_id == Exercise.id)
            .join(Student, WaitRoom.student_id == Student.id)
            .with_entities(Exercise.id.label("exercise_id"), Exercise.subject_name, Exercise.group_name, WaitRoom.student_id, Student)
            .all()
        )

        # Organize the data
        exercise_group_data = {}

        for result in results:
            exercise_id = result.exercise_id
            subject_name = result.subject_name
            group_name = result.group_name
            student_id = result.student_id
            student = result[4]  # The Student object

            # Convert student to dictionary
            student_dict = student.to_dict()

            # Initialize the exercise entry if needed
            if exercise_id not in exercise_group_data:
                exercise_group_data[exercise_id] = {"exercise_id": exercise_id, "subject_name": subject_name, "group_ids": []}

            # Find the group entry or create a new one
            group_entry = None
            for group in exercise_group_data[exercise_id]["group_ids"]:
                if group["group_name"] == group_name:
                    group_entry = group
                    break

            if not group_entry:
                group_entry = {"group_name": group_name, "students_data": []}
                exercise_group_data[exercise_id]["group_ids"].append(group_entry)

            # Add student data
            group_entry["students_data"].append({"student_id": student_id, "student_data": student_dict})

        return exercise_group_data

    @staticmethod
    def add_to_wait_room(student_id: int, exercise_ids: List[int], group_id: str) -> bool:
        """
        Add a student's exercises to the wait room.

        Args:
            student_id: The student ID
            exercise_ids: List of exercise IDs to add
            group_id: The group ID

        Returns:
            True if successful, False otherwise
        """
        for exercise_id in exercise_ids:
            # Check if already in wait room
            existing = WaitRoom.query.filter_by(student_id=student_id, exercise_id=exercise_id).first()

            if not existing:
                wait_entry = WaitRoom(student_id=student_id, group_id=group_id, exercise_id=exercise_id)
                wait_entry.save()

                # Update exercise check type
                exercise = Exercise.query.get(exercise_id)
                if exercise:
                    exercise.checkkType = 1
                    exercise.save()

        return True

    @staticmethod
    def remove_from_wait_room(exercise_id: int, student_id: int) -> bool:
        """
        Remove a student's exercise from the wait room.

        Args:
            exercise_id: The exercise ID
            student_id: The student ID

        Returns:
            True if successful, False otherwise
        """
        wait_entry = WaitRoom.query.filter_by(exercise_id=exercise_id, student_id=student_id).first()

        if wait_entry:
            wait_entry.delete()
            return True

        return False

    @staticmethod
    def complete_exercise(exercise_id: int, student_id: int, rating_value: int) -> bool:
        """
        Complete an exercise, remove from wait room, and update student rating.

        Args:
            exercise_id: The exercise ID
            student_id: The student ID
            rating_value: The rating value to add to the student

        Returns:
            True if successful, False otherwise
        """
        # Remove from wait room
        wait_entry = WaitRoom.query.filter_by(exercise_id=exercise_id, student_id=student_id).first()

        if wait_entry:
            wait_entry.delete()

            # Remove exercise from group
            ExerciseGroup.query.filter_by(exercise_id=exercise_id, group_name="Group A").delete()  # This was hardcoded in the original

            # Update student rating
            student = Student.query.get(student_id)
            if student:
                student.rating = (student.rating or 0) + rating_value
                student.save()

            return True

        return False
