from flask import flash, jsonify, redirect, render_template, request, session, url_for

from app.services.file_service import FileService
from app.services.subject_service import SubjectService


class SubjectController:
    @staticmethod
    def list_subjects():
        if not session.get("logged_in"):
            return redirect(url_for("auth.login"))

        group_ids = session.get("group_ids")
        subject_service = SubjectService()
        file_service = FileService()

        subject_data = subject_service.get_subjects_by_groups(group_ids)

        # Build hierarchical data structure
        data = []
        for subject in subject_data:
            subject_id = subject["subject_id"]
            files = file_service.get_files_by_subject(subject_id)

            file_data = [
                {
                    "file_name": file["file_name"],
                    "file_type": file_service.get_file_extension(file["file_name"]),
                    "subject_id": subject_id,
                    "file_id": file["id"],
                }
                for file in files
            ]

            subject_info = {"subject_name": subject["subject_name"], "files": file_data}
            data.append(subject_info)

        return render_template("subjects.html", file_data=data)

    @staticmethod
    def add_subject():
        if request.method == "POST":
            subject_service = SubjectService()
            file_service = FileService()

            subject_data = {"group_name": request.form["group_name"], "subject_name": request.form["subject_name"], "messenge": request.form.get("messenge", "")}

            subject_id = subject_service.add_subject(subject_data)

            # Handle file upload if present
            if "file" in request.files and request.files["file"].filename:
                file = request.files["file"]
                file_name = file.filename
                file_data = file.read()

                file_service.add_file_to_subject(subject_id, file_name, file_data)

            flash("Subject added successfully", "success")
            return redirect(url_for("subjects.list"))

        return render_template("add-subject.html")

    @staticmethod
    def edit_subject(id):
        subject_service = SubjectService()

        if request.method == "POST":
            subject_data = {"group_name": request.form["group_name"], "subject_name": request.form["subject_name"], "messenge": request.form.get("messenge", "")}

            subject_service.update_subject(id, subject_data)

            # Handle file upload if present
            if "file" in request.files and request.files["file"].filename:
                file_service = FileService()
                file = request.files["file"]
                file_name = file.filename
                file_data = file.read()

                file_service.add_file_to_subject(id, file_name, file_data)

            flash("Subject updated successfully", "success")
            return redirect(url_for("subjects.list"))

        subject = subject_service.get_subject_by_id(id)
        return render_template("edit-subject.html", data=subject)

    @staticmethod
    def delete_subject_file(subject_id, file_id):
        file_service = FileService()
        file_service.remove_file_from_subject(subject_id, file_id)
        flash("File removed from subject", "success")
        return redirect(url_for("subjects.list"))
