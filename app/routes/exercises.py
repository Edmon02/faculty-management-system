# app/routes/exercises.py
from datetime import datetime

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for

from app.services.exercise_service import ExerciseService
from app.utils.helpers import login_required

exercises_bp = Blueprint("exercises", __name__)


@exercises_bp.route("/exercises", methods=["POST", "GET"])
@login_required
def exercises_list():
    group_ids = session["group_ids"]
    exercise_service = ExerciseService()

    exercise_data = exercise_service.get_exercises_by_groups(group_ids)

    if session["type"] == "student":
        checkTypes = exercise_service.get_waiting_exercises(session["ID"])
        for exercise in exercise_data:
            exercise["checkType"] = 1 if exercise["id"] in checkTypes else 0

    exercise_data = [
        {
            "id": data["id"],
            "group_name": data["group_name"],
            "expiry_time": data["expiry_time"],
            "subject_name": data["subject_name"],
            "messenge": data["messenge"],
            "checkType": data.get("checkType", 0),
            "file_name": data["file_name"],
            "file_type": os.path.splitext(data["file_name"])[1],
        }
        for data in exercise_data
    ]

    return render_template("exercises.html", data=exercise_data)


@exercises_bp.route("/add-exercise", methods=["GET", "POST"])
@login_required
def add_exercise():
    exercise_service = ExerciseService()

    if request.method == "POST":
        end_time = datetime.strptime(request.form["end_time"], "%Y-%m-%d")
        group_name = request.form["group_name"]
        messenge = request.form["messenge"]
        subject_name = request.form["subject_name"]
        file = request.files["file"].read()
        file_name = request.files["file"].filename

        exercise_service.add_exercise(end_time, group_name, messenge, subject_name, file_name, file)

    return render_template("add-exercise.html")


@exercises_bp.route("/edit-exercise/<int:id>", methods=["GET", "POST"])
@login_required
def edit_exercise(id):
    exercise_service = ExerciseService()
    data_cursor = exercise_service.get_exercise_by_id(id)

    expiry_time = datetime.strptime(data_cursor["expiry_time"], "%Y-%m-%d")
    data_cursor["expiry_time"] = "{:%Y-%m-%d}".format(expiry_time)

    if request.method == "POST":
        search_params = dict(data_cursor)
        filename = request.files["file_name"].filename if "file_name" in request.files else ""

        # Extract form data and update search_params dictionary
        search_params["group_name"] = request.form["group_name"]
        search_params["expiry_time"] = request.form["expiry_time"]
        search_params["subject_name"] = request.form["subject_name"]
        search_params["messenge"] = request.form.get("messenge")
        search_params["file_name"] = data_cursor["file_name"] if not filename else filename

        # Update the exercise record in the database
        exercise_service.update_exercise(id, search_params)

        # Redirect the user to the exercise list page
        return redirect(url_for("exercises.exercises_list"))

    return render_template("edit-exercise.html", data=data_cursor)


@exercises_bp.route("/delete-exercise/<int:id>", methods=["GET", "POST"])
@login_required
def delete_exercise(id):
    exercise_service = ExerciseService()

    if request.method == "GET":
        exercise_service.delete_exercise(id)

    return redirect(url_for("exercises.exercises_list"))


@exercises_bp.route("/waitroom", methods=["GET", "POST"])
@login_required
def waitroom():
    exercise_service = ExerciseService()

    if request.method == "POST":
        data = request.json
        user_id = session["ID"]
        selected_ids = data.get("selectedIds", [])
        group_id = session["group_ids"][0]

        if exercise_service.insert_into_waitroom(user_id, selected_ids, group_id):
            return jsonify({"message": "Data sent to WaitRoom successfully"})
        else:
            return jsonify({"error": "Failed to insert data into WaitRoom"})

    return redirect(url_for("exercises.exercises_list"))


@exercises_bp.route("/waitingroom", methods=["GET", "POST"])
@login_required
def waiting_room():
    exercise_service = ExerciseService()
    exercise_group_data = exercise_service.get_waiting_room_data()

    return render_template("waitingroom.html", datas=exercise_group_data)


@exercises_bp.route("/outwaitingroom/<int:id1>/<int:id2>", methods=["GET", "POST"])
@login_required
def out_waiting_room(id1, id2):
    exercise_service = ExerciseService()
    exercise_service.remove_from_waiting_room(id1, id2)

    return redirect(url_for("exercises.waiting_room"))


@exercises_bp.route("/done/<int:exercise_id>/<int:student_id>/<int:selected_value>", methods=["GET", "POST"])
@login_required
def done(exercise_id, student_id, selected_value):
    exercise_service = ExerciseService()
    exercise_service.complete_exercise(exercise_id, student_id, selected_value)

    return redirect(url_for("exercises.waiting_room"))


@exercises_bp.route("/check_exercises_changes", methods=["GET"])
def check_exercises_changes_route():
    exercise_service = ExerciseService()

    if session.get("group_ids", None):
        group_name = session["group_ids"][0]
        exercises = exercise_service.check_exercises_changes(group_name)
        return jsonify(exercises)

    return jsonify("you are not logged in"), 500
