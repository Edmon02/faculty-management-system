import base64
import os
from datetime import datetime

import pandas as pd
from flask import flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from app.models.student import Student
from app.services.file_service import FileService
from app.services.student_service import StudentService
from app.utils.security import allowed_file


class StudentController:
    @staticmethod
    def list_students():
        if not session.get("logged_in"):
            return redirect(url_for("auth.login"))

        group_ids = session.get("group_ids")
        student_service = StudentService()
        data_student = student_service.get_students_by_groups(group_ids)

        # Handle search filtering
        if request.method == "GET" and any(request.args.values()):
            search_params = {
                "id": request.args.get("id", default="", type=str),
                "first_name": request.args.get("first_name", default="", type=str),
                "phone": request.args.get("phone", default="", type=str),
            }

            data_student = student_service.filter_students(data_student, search_params)

        # Handle sorting
        if request.method == "POST" and request.form.get("action") == "Sort":
            data_student = sorted(data_student, key=lambda x: x["rating"], reverse=True)

        return render_template("students.html", data=data_student)

    @staticmethod
    def add_student():
        if request.method == "POST":
            student_service = StudentService()
            file_service = FileService()

            if "excel_file" in request.files and request.files["excel_file"].filename:
                excel_file = request.files["excel_file"]
                df = pd.read_excel(excel_file)

                for _, row in df.iterrows():
                    student_data = {
                        "first_name": row["Name"],
                        "last_name": row["Surname"],
                        "patronymic": row["Patronymic"],
                        "phone": row["Phone"],
                        "address": "",
                        "birthday_date": row["Birthday"].to_pydatetime(),
                        "group_name": row["Group"],
                    }
                    student_service.add_student(student_data)

                flash("Students added successfully from Excel file", "success")
                return redirect(url_for("students.list"))

            # Handle single student addition
            photo_data = None
            if "photo" in request.files and request.files["photo"].filename:
                photo = request.files["photo"]
                if photo and allowed_file(photo.filename, {"png", "jpg", "jpeg", "gif"}):
                    photo_data = photo.read()
            else:
                # Use default image
                with open(os.path.join("app", "static", "images", "default_avatar.jpg"), "rb") as f:
                    photo_data = f.read()

            student_data = {
                "first_name": request.form["first_name"],
                "last_name": request.form["last_name"],
                "patronymic": request.form["patronymic"],
                "phone": request.form["phone"],
                "address": "",
                "birthday_date": datetime.strptime(request.form["dob"], "%Y-%m-%d"),
                "group_name": request.form["group"],
                "image": photo_data,
            }

            student_service.add_student(student_data)
            flash("Student added successfully", "success")
            return redirect(url_for("students.list"))

        return render_template("add-student.html")

    @staticmethod
    def edit_student(id):
        student_service = StudentService()

        if request.method == "POST":
            student_data = {
                "last_name": request.form["last_name"],
                "first_name": request.form["first_name"],
                "patronymic": request.form["patronymic"],
                "birthday_date": request.form["dob"],
                "group_name": request.form.get("group_name"),
                "phone": request.form["phone"],
            }

            student_service.update_student(id, student_data)
            flash("Student updated successfully", "success")
            return redirect(url_for("students.list"))

        student = student_service.get_student_by_id(id)
        return render_template("edit-student.html", data=student)
