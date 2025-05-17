from datetime import datetime

from flask import flash, jsonify, redirect, render_template, request, session, url_for

from app.services.exercise_service import ExerciseService
from app.services.file_service import FileService


class ExerciseController:
    @staticmethod
    def list_exercises():
        if not session.get("logged_in"):
            return redirect(url_for("auth.login"))

        group_ids = session.get("group_ids")
        exercise_service = ExerciseService()

        exercise_data = exercise_service.get_exercises_by_groups(group_ids)

        # Mark exercises that are in waitroom for current student
        if session["type"] == "student":
            student_id = session["ID"]
            waitroom_exercises = exercise_service.get_waitroom_exercises(student_id)

            for exercise in exercise_data:
                exercise["checkType"] = 1 if exercise["id"] in waitroom_exercises else 0

        return render_template("exercises.html", data=exercise_data)

    @staticmethod
    def add_exercise():
        if request.method == "POST":
            exercise_service = ExerciseService()
            file_service = FileService()

            end_time = datetime.strptime(request.form["end_time"], "%Y-%m-%d")
            group_name = request.form["group_name"]
            messenge = request.form["messenge"]
            subject_name = request.form["subject_name"]

            # Handle file upload
            file_name = ""
            file_data = None
            if "file" in request.files and request.files["file"].filename:
                file = request.files["file"]
                file_name = file.filename
                file_data = file.read()

            # Calculate expiry time
            delta = datetime.now() - end_time
            expiry_time = (datetime.now() + delta).strftime("%Y-%m-%d")

            exercise_data = {"expiry_time": expiry_time, "messenge": messenge, "subject_name": subject_name, "file_name": file_name}

            # Save exercise and associate with group
            exercise_id = exercise_service.add_exercise(exercise_data, group_name)

            # Add file to subject if necessary
            if file_data and file_name:
                # Get subject_id from subject_name
                subject_id = exercise_service.get_subject_id_by_name(subject_name)
                if subject_id:
                    file_service.add_file_to_subject(subject_id, file_name, file_data)

            flash("Exercise added successfully", "success")
            return redirect(url_for("exercises.list"))

        return render_template("add-exercise.html")

    @staticmethod
    def edit_exercise(id):
        exercise_service = ExerciseService()

        if request.method == "POST":
            # Get file name from uploaded file or keep existing
            filename = ""
            if "file" in request.files and request.files["file"].filename:
                filename = request.files["file"].filename

            exercise_data = {
                "group_name": request.form["group_name"],
                "expiry_time": request.form["expiry_time"],
                "subject_name": request.form["subject_name"],
                "messenge": request.form.get("messenge", ""),
                "file_name": filename or request.form.get("current_file_name", ""),
            }

            exercise_service.update_exercise(id, exercise_data)

            # Handle file upload if new file
            if filename:
                file_service = FileService()
                file_data = request.files["file"].read()
                subject_id = exercise_service.get_subject_id_by_name(exercise_data["subject_name"])

                if subject_id:
                    file_service.add_file_to_subject(subject_id, filename, file_data)

            flash("Exercise updated successfully", "success")
            return redirect(url_for("exercises.list"))

        exercise = exercise_service.get_exercise_by_id(id)
        return render_template("edit-exercise.html", data=exercise)

    @staticmethod
    def delete_exercise(id):
        exercise_service = ExerciseService()
        exercise_service.delete_exercise(id)
        flash("Exercise deleted successfully", "success")
        return redirect(url_for("exercises.list"))

    @staticmethod
    def waitroom():
        if request.method == "POST":
            data = request.json
            user_id = session.get("ID", 0)
            selected_ids = data.get("selectedIds", [])
            group_id = session.get("group_ids", [])[0] if session.get("group_ids") else 0

            exercise_service = ExerciseService()
            success = exercise_service.add_to_waitroom(user_id, selected_ids, group_id)

            if success:
                return jsonify({"message": "Data sent to WaitRoom successfully"})
            else:
                return jsonify({"error": "Failed to insert data into WaitRoom"}), 500

        return redirect(url_for("exercises.list"))

    @staticmethod
    def waiting_room():
        exercise_service = ExerciseService()
        exercise_group_data = exercise_service.get_waiting_room_data()

        return render_template("waitingroom.html", datas=exercise_group_data)

    @staticmethod
    def out_waiting_room(exercise_id, student_id):
        exercise_service = ExerciseService()
        exercise_service.remove_from_waitroom(exercise_id, student_id)

        flash("Student removed from waiting room", "success")
        return redirect(url_for("exercises.waiting_room"))

    @staticmethod
    def done(exercise_id, student_id, selected_value):
        exercise_service = ExerciseService()
        exercise_service.complete_exercise(exercise_id, student_id, selected_value)

        flash(f"Exercise marked as complete with rating {selected_value}", "success")
        return redirect(url_for("exercises.waiting_room"))
