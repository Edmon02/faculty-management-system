# app/routes/students.py
from datetime import datetime

import pandas as pd
from flask import Blueprint, redirect, render_template, request, session, url_for

from app.services.student_service import StudentService
from app.utils.helpers import login_required

students_bp = Blueprint("students", __name__)


@students_bp.route("/students", methods=["GET", "POST"])
@login_required
def students_list():
    group_ids = session.get("group_ids")
    student_service = StudentService()

    data_student = student_service.get_all_students_by_groups(group_ids)

    if request.method == "GET":
        search_params = {}

        # Extract query parameters and update search_params dictionary
        search_params["id"] = request.args.get("id", default="", type=str)
        search_params["first_name"] = request.args.get("first_name", default="", type=str)
        search_params["phone"] = request.args.get("phone", default="", type=str)

        # Filter Data_student based on search_params
        if search_params["id"]:
            data_student = [data for data in data_student if search_params["id"] in data["_id"]]
        if search_params["first_name"]:
            data_student = [data for data in data_student if search_params["first_name"].lower() == data["first_name"].lower()]
        if search_params["phone"]:
            data_student = [data for data in data_student if search_params["phone"] in data["phone"]]

    if request.method == "POST" and request.form["action"] == "Sort":
        data_student = sorted(data_student, key=lambda x: x["rating"], reverse=True)

    return render_template("students.html", data=data_student)


@students_bp.route("/students/add-student", methods=["GET", "POST"])
@login_required
def add_student():
    student_service = StudentService()

    if request.method == "POST":
        # Handle Excel file upload
        excel_file = request.files.get("excel_file")
        if excel_file:
            df = pd.read_excel(excel_file)
            # Iterate through rows and insert into the database
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
                student_service.insert_student_data(student_data)

            return redirect(url_for("students.students_list"))

        # Handle single student addition
        photo = request.files.get("photo")
        if photo:
            picture_data = photo.read()
        else:
            # Use default image
            with open("static/images/default.jpg", "rb") as f:
                picture_data = f.read()

        student_data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "patronymic": request.form["patronymic"],
            "phone": request.form["phone"],
            "address": "",
            "birthday_date": datetime.strptime(request.form["dob"], "%Y-%m-%d"),
            "group_name": request.form["group"],
            "image": picture_data,
        }

        student_service.insert_student_data(student_data)
        return redirect(url_for("dashboard.dashboard"))

    return render_template("add-student.html")


@students_bp.route("/students/edit-student/<int:id>", methods=["GET", "POST"])
@login_required
def edit_student(id):
    student_service = StudentService()
    data_cursor = student_service.get_student_by_id(id)

    if request.method == "POST":
        search_params = dict(data_cursor)

        # Extract form data and update search_params dictionary
        search_params["last_name"] = request.form["last_name"]
        search_params["first_name"] = request.form["first_name"]
        search_params["patronymic"] = request.form["patronymic"]
        search_params["birthday_date"] = request.form["dob"]
        search_params["group_name"] = request.form.get("group_name", default=data_cursor["group_name"], type=int)
        search_params["phone"] = request.form["phone"]

        # Update the student record in the database
        student_service.update_student(id, search_params, data_cursor)

        # Redirect the user to the student list page
        return redirect(url_for("students.students_list"))

    return render_template("edit-student.html", data=data_cursor)


@students_bp.route("/find-thesis", methods=["GET", "POST"])
@login_required
def find_thesis():
    student_service = StudentService()

    if request.method == "POST":
        large_text = request.form["thesis_title"]
        data_student = student_service.find_similar_thesis(large_text)
        return jsonify(data_student)

    return render_template("find-sim-thesis.html")
