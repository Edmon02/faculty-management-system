import base64
import sqlite3

from flask import jsonify, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.student_service import StudentService
from app.services.thesis_service import ThesisService


class ThesisController:
    @staticmethod
    def find_thesis():
        if request.method == "POST":
            thesis_service = ThesisService()
            student_service = StudentService()

            thesis_title = request.form["thesis_title"]

            # Find similar theses based on text similarity
            similar_topics = thesis_service.find_similar_theses(thesis_title)

            # Get student data for similar theses
            data_student = []
            if similar_topics:
                data_student = student_service.get_students_by_ids(similar_topics)

                # Add thesis data to students
                thesis_mapping = thesis_service.get_thesis_student_mapping()
                for student in data_student:
                    student_id = student["id"]
                    thesis_id = thesis_mapping.get(student_id)
                    if thesis_id:
                        student["thesis"] = thesis_id

                # Convert binary image data to base64
                for item in data_student:
                    if "image" in item and item["image"]:
                        item["image"] = base64.b64encode(item["image"]).decode("utf-8")

            return jsonify(data_student)

        return render_template("find-sim-thesis.html")
