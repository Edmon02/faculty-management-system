# app/routes/subjects.py
import os

from flask import Blueprint, make_response, redirect, render_template, request, session, url_for

from app.services.file_service import FileService
from app.services.subject_service import SubjectService
from app.utils.helpers import login_required

subjects_bp = Blueprint("subjects", __name__)


@subjects_bp.route("/subjects", methods=["GET", "POST"])
@login_required
def subjects_list():
    group_ids = session["group_ids"]
    subject_service = SubjectService()

    subject_data = subject_service.get_subjects_by_groups(group_ids)

    data = []
    for subject in subject_data:
        subject_id = subject["subject_id"]
        file_data = subject_service.get_files_by_subject_id(subject_id)
        subject_data = {"subject_name": subject["subject_name"], "files": file_data}
        data.append(subject_data)

    return render_template("subjects.html", file_data=data)


@subjects_bp.route("/add-subject", methods=["GET", "POST"])
@login_required
def add_subject():
    subject_service = SubjectService()

    if request.method == "POST":
        group_name = request.form["group_name"]
        subject_name = request.form["subject_name"]
        file = request.files.get("file")

        subject_service.add_subject(group_name, subject_name, file)

    return render_template("add-subject.html")


@subjects_bp.route("/edit-subject/<int:id>", methods=["GET", "POST"])
@login_required
def edit_subject(id):
    return render_template("edit-subject.html")


@subjects_bp.route("/delte-subject/<int:id1>/<int:id2>", methods=["GET", "POST"])
@login_required
def delete_subject(id1, id2):
    subject_service = SubjectService()

    if request.method == "GET":
        subject_service.delete_subject_file(id1, id2)

    return redirect(url_for("subjects.subjects_list"))


@subjects_bp.route("/file")
@login_required
def show_file():
    filename = request.args.get("filename")
    file_service = FileService()

    response = file_service.get_file_response(filename)
    if isinstance(response, make_response):
        return response
    else:
        return response
