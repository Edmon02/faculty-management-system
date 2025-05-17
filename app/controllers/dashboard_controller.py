import pandas as pd
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure
from flask import redirect, render_template, session, url_for

# from app.services.dashboard_service import DashboardService
from app.services.file_service import FileService
from app.services.student_service import StudentService
from app.services.subject_service import SubjectService


class DashboardController:
    @staticmethod
    def show_dashboard():
        if not session.get("logged_in"):
            return redirect(url_for("auth.login"))

        ID = session.get("ID")
        group_ids = session.get("group_ids")

        student_service = StudentService()
        subject_service = SubjectService()
        file_service = FileService()
        # dashboard_service = DashboardService()

        # Get student data grouped by groups
        rows = student_service.get_students_by_groups(group_ids)

        # Organize students by groups
        group_data = {}
        for row in rows:
            group_name = row["group_name"]

            if group_name not in group_data:
                group_data[group_name] = {
                    "group_name": group_name,
                    "student_datas": [row],
                }
            else:
                group_data[group_name]["student_datas"].append(row)

        data = {"group_datas": group_data}

        # Get subject and file data for student view
        if session["type"] == "student":
            subject_data = subject_service.get_subjects_for_student(group_ids)
            file_datas = []

            for subject in subject_data:
                subject_id = subject["subject_id"]
                files = file_service.get_files_by_subject(subject_id)

                file_data = [
                    {
                        "file_name": file["file_name"],
                        "file_type": file_service.get_file_extension(file["file_name"]),
                        "file_id": file["id"],
                    }
                    for file in files
                ]

                subject_info = {
                    "subject_name": subject["subject_name"],
                    "files": file_data,
                }
                file_datas.append(subject_info)

            data["files"] = file_datas

        # Get user activity data for chart
        # user_data = dashboard_service.get_user_activity_data()

        # Create Bokeh chart for user activity
        user_df = pd.DataFrame(["user_data"])
        user_df["date"] = pd.to_datetime(user_df["date"])

        p = figure(
            title="User Activity Over Time",
            x_axis_label="Date",
            y_axis_label="Activity Count",
            x_axis_type="datetime",
            max_height=400,
        )

        # Configure axis formatting
        p.xaxis[0].ticker.desired_num_ticks = len(user_df["date"].unique())
        p.xaxis[0].formatter = DatetimeTickFormatter(months="%b %Y")

        # Plot the line
        p.line(user_df["date"], user_df["activity_count"], legend_label="User Activity")
        p.legend.location = "top_left"

        # Get script and div components for embedding
        script, div = components(p)

        return render_template("dashboard.html", data=data, script=script, div=div)
