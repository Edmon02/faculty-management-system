# app/routes/dashboard.py
import pandas as pd
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure
from flask import Blueprint, redirect, render_template, session, url_for

from app.services.student_service import StudentService
from app.services.subject_service import SubjectService
from app.utils.helpers import login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    ID = session.get("ID")
    student_service = StudentService()
    subject_service = SubjectService()

    # Get student data by groups
    group_ids = tuple(session["group_ids"])
    data = {}
    data["group_datas"] = student_service.get_students_by_groups(group_ids)

    if session["type"] == "student":
        file_datas = subject_service.get_subject_files_for_student(group_ids)
        data["files"] = file_datas

    # Get user activity data for visualization
    # user_data = get_user_activity_data()

    # Convert the data to a DataFrame
    user_data = pd.DataFrame(["user_data"])

    # Convert 'date' to datetime format
    user_data["date"] = pd.to_datetime(user_data["date"])

    # Create a Bokeh figure
    p = figure(
        title="User Activity Over Time",
        x_axis_label="Date",
        y_axis_label="Activity Count",
        x_axis_type="datetime",
        max_height=400,
    )

    # Configure the x-axis ticker to show monthly ticks
    p.xaxis[0].ticker.desired_num_ticks = len(user_data["date"].unique())
    p.xaxis[0].formatter = DatetimeTickFormatter(months="%b %Y")

    # Plot the line
    p.line(user_data["date"], user_data["activity_count"], legend_label="User Activity")

    # Customize the plot if needed
    p.legend.location = "top_left"

    # Get the script and div components for embedding
    script, div = components(p)

    return render_template("dashboard.html", data=data, script=script, div=div)


@dashboard_bp.route("/roadmap")
def roadmap():
    return render_template("index.html")


@dashboard_bp.route("/about-us")
def about_us():
    return render_template("index.html")


@dashboard_bp.route("/contact")
def contact():
    return render_template("index.html")
