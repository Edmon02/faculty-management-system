from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash, get_flashed_messages, jsonify#, send_from_directory, send_file,
from flask_wtf import FlaskForm
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired
import random
import string
import hashlib
import secrets
import base64
from io import BytesIO
import os
#from werkzeug.utils import secure_filename
from openpyxl import Workbook
import mimetypes
import sqlite3
from functools import cache
from datetime import datetime, timedelta

# Define login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddSubjectForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    group = SelectField('group', choices=[('1', '1'), ('2', '2'), ('3', '3')], validators=[DataRequired()])
    file = FileField('file', validators=[DataRequired()])
    submit = SubmitField('Submit')


def random_numbers(length):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def random_password(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

UPLOAD_FOLDER = 'c:\\Users\\edmon\\Downloads\\Telegram Desktop\\Polytech_Univ\\'

app = Flask(__name__)

secret_key = secrets.token_hex(16)
app.secret_key = secret_key

# Set secure configurations
# app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = '/static/images'

cur_dir = os.path.dirname(__file__)
# Define the SQLite database path
DATABASE =  os.path.join(cur_dir, 'pulpit.sqlite')

DATABASE2 = os.path.join(cur_dir, 'pulpit.db')

# Set up rate limiting
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

# Set session configurations
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'

# Set the lifetime of a permanent session
app.permanent_session_lifetime = 3600  # seconds


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if bool(form.username.data and form.password.data) and 'logged_in' not in session :
        username = form.username.data
        password = form.password.data
        query = "SELECT * FROM Users WHERE username = ? AND password = ?"
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        conn2 = sqlite3.connect(DATABASE2)
        cursor2 = conn2.cursor()

        cursor.execute(query, (username, password))

        # Fetch the first row
        result = cursor.fetchone()
        # print(result)

        if result is not None:
            column_names = [description[0] for description in cursor.description]

            # Fetch the results
            user_data = dict(zip(column_names, result))
            query = "SELECT * FROM Student WHERE id = ?" if user_data['type']=='student' else "SELECT * FROM Lecturer WHERE id = ?"

            cursor.execute(query, (user_data['_id'], ))
            # Get the column names
            column_names = [description[0] for description in cursor.description]

            # Fetch the results
            data = dict(zip(column_names, cursor.fetchone()))
            # print(data)

            if user_data['type'] == 'lecturer':
                query = """
                        SELECT
                            group_id
                        FROM LecturerGroup lg
                        WHERE lg.lecturer_id = ?;
                        """
                cursor2.execute(query, (data['id'], ) )
                # Fetch the results
                group_ids = [result[0] for result in cursor2.fetchall()]
                print(group_ids)
            else : group_ids = str(data['group_id'])

        cursor2.close()
        conn2.close()
        cursor.close()
        conn.close()
        if result is not None and data:
            # student_id = data[0]
            hashed_password = data['password']

            session['logged_in'] = True
            session['type'] = user_data['type']
            session['first_name'] = data['first_name']
            session['last_name'] = data['last_name']
            session['is_Admin'] = data['is_Admin']
            session['ID'] = data['id']
            session['group_ids'] = group_ids if isinstance(group_ids, list) else (int(group_ids), )
            return jsonify({'message': 'Login successful'})

    return render_template('index.html', form=form)

@app.route('/roadmap')
def roadmap():
    return render_template('roadmap.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit('5 per minute')
def login():
    form = LoginForm()
    if form.validate_on_submit() and 'logged_in' not in session :
        username = form.username.data
        password = form.password.data
        query = {'username': username, "password":password}
        data_cursor = list(students.find(query))
        if len(data_cursor) == 0:
            data_cursor = list(lecturer.find(query))
        data_list = data_cursor
        if len(data_list) == 1:
            hashed_password = data_list[0]['password']
            # if bcrypt.checkpw(password.encode(), hashed_password.encode()):
            session['logged_in'] = True
            session['group_id'] = data_list[0]['group_id']
            session['first_name'] = data_list[0]['first_name']
            session['last_name'] = data_list[0]['last_name']
            session['is_Admin'] = data_list[0]['is_Admin']
            session['username'] = username
            session['password'] = hashed_password

            return redirect(url_for('dashboard'))
            # else:
            #     flash('Invalid username or password', 'danger')
        else:
            flash('Invalid username or password', 'danger')
    elif 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect to the login page
    return redirect(url_for('index'))

@cache
@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        ID = session.get('ID')
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # # Retrieve student data from SQLite
        # query = "SELECT * FROM Student WHERE id = ? "
        # cursor.execute(query, (ID, ))
        # # Get the column names
        # column_names = [description[0] for description in cursor.description]

        # # Fetch the results
        # data = [dict(zip(column_names, cursor.fetchone()))]

        group_ids = tuple(session['group_ids'])
        query = """
        SELECT g.group_name, s.*
        FROM Groups g
        LEFT JOIN Student s ON g.id = s.group_id
        WHERE g.id IN ({})
        """.format(','.join('?' for _ in group_ids))

        cursor.execute(query, group_ids)
        column_names = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        group_data = {}

        for row in rows:
            group_name = row[0]
            student_data = dict(zip(column_names[1:], row[1:]))

            if group_name not in group_data:
                group_data[group_name] = {
                    'group_name': group_name,
                    'student_datas': [student_data]
                }
            else:
                group_data[group_name]['student_datas'].append(student_data)

        data = {}
        data['group_datas'] = group_data

        if session['type'] == 'student':

            conn2 = sqlite3.connect(DATABASE2)
            cursor2 = conn2.cursor()

            query2 = """
            SELECT s.subject_id, s.subject_name
            FROM Subject s
            WHERE s.subject_id IN (
                SELECT slg.subject_id
                FROM SubjectLecturerGroup slg
                WHERE slg.lecturer_id IN (
                    SELECT lecturer_id
                    FROM Lecturer
                    WHERE lecturer_id IN (
                        SELECT lecturer_id
                        FROM SubjectLecturerGroup
                        WHERE group_id in (?)
                    )
                )
            );
            """

            cursor2.execute(query2, session['group_ids'])
            column_names2 = [description[0] for description in cursor2.description]
            subject_data = [dict(zip(column_names2, row)) for row in cursor2.fetchall()]
            file_datas = []
            for subject in subject_data:
                subject_id = subject['subject_id']
                query = "SELECT * FROM Files WHERE subject_id = ?"
                cursor.execute(query, (subject_id,))
                column_names = [description[0] for description in cursor.description]
                files = [dict(zip(column_names, row)) for row in cursor.fetchall()]
                file_data = [{
                    'file_name': file['file_name'],
                    'file_type': os.path.splitext(file['file_name'])[1]
                } for file in files]
                subject_data = {
                    'subject_name': subject['subject_name'],
                    'files': file_data
                }
                file_datas.append(subject_data)
            data['files'] = file_datas
            cursor.close()
            cursor2.close()
            conn2.close()


        conn.close()

        return render_template('dashboard.html', data=data)
    else:
        return redirect(url_for('index'))

@app.route('/students', methods=['GET', 'POST'])
def studentsList():
    if 'logged_in' in session:
        group_ids = session.get('group_ids')

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Retrieve student data from SQLite based on group_id
        query = "SELECT * FROM Student WHERE group_id in ({})".format(','.join('?' for _ in group_ids))
        cursor.execute(query, group_ids)
        # Get the column names
        column_names = [description[0] for description in cursor.description]

        # Fetch the results
        data_student = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        conn.close()

        if request.method == 'GET':
            search_params = {}

            # Extract query parameters and update search_params dictionary
            search_params['id'] = request.args.get('id', default='', type=str)
            search_params['first_name'] = request.args.get('first_name', default='', type=str)
            search_params['phone'] = request.args.get('phone', default='', type=str)

            # Filter Data_student based on search_params
            if search_params['id']:
                data_student = [data for data in data_student if search_params['id'] in data['_id']]
            if search_params['first_name']:
                data_student = [data for data in data_student if search_params['first_name'].lower() == data['first_name'].lower()]
            if search_params['phone']:
                data_student = [data for data in data_student if search_params['phone'] in data['phone']]


        if request.method == 'POST' and request.form['action'] == 'Sort':
            data_student = sorted(data_student, key=lambda x: x['rating'], reverse=True)

        return render_template('students.html', data=data_student)
    else:
        return redirect(url_for('login'))

@app.route('/students/add-student', methods=['GET', 'POST'])
def addStudent():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        # gender = request.form['gender']
        dob = request.form['dob']
        group_id = int(request.form['group'])
        # blood_group = request.form.get('blood_group')
        religion = request.form['patronymic']
        email = request.form['email']
        # class_name = request.form.get('class_name')
        # section = request.form.get('section')
        # admission_id = request.form['address']
        phone = request.form['phone']
        file = request.files['photo']
        if file:
            picture_data = file.read()
        else:
            # Open the image file and read its contents
            with open("images.jpg", "rb") as f:
                image_data = f.read()

            # Encode the image data as base64
            picture_data = base64.b64encode(image_data)
            # If no file was uploaded, use a default photo
            # db.students.insert_one({'photo_path': 'default.png'})


        password = random_password(10)

        # hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(password)

        # Connect to the SQLite database
        conn = sqlite3.connect('pulpit.sqlite')
        cursor = conn.cursor()

        # Prepare the SQL query and data
        query = "INSERT INTO Student (group_id, first_name, last_name, patronymic, birthday_date,phone, username, password, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        data = (group_id, first_name, last_name, religion, dob, phone, random_numbers(8), hashed_password, picture_data)

        # Execute the query
        cursor.execute(query, data)
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))
    else:
        return render_template('add-student.html')

@app.route('/students/edit-student/<int:id>', methods=['GET', 'POST'])
def editStudent(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = "SELECT * FROM Student WHERE id = ?"
    cursor.execute(query, (id,))
    # Get the column names
    column_names = [description[0] for description in cursor.description]

    # Fetch the results
    data_cursor = dict(zip(column_names, cursor.fetchone()))
    print(data_cursor['id'])
    if request.method == 'POST':
        search_params = dict(data_cursor)

        # Extract form data and update search_params dictionary
        search_params['last_name'] = request.form['last_name']
        search_params['first_name'] = request.form['first_name']
        search_params['patronymic'] = request.form['patronymic']
        search_params['birthday_date'] = request.form['dob']
        search_params['group_id'] = request.form.get('group_id', default=data_cursor['group_id'], type=int)
        search_params['phone'] = request.form['phone']

        # Update the student record in the database
        old_data = data_cursor
        if old_data != search_params:
            update_query = "UPDATE Student SET last_name = ?, first_name = ?, patronymic = ?, birthday_date = ?, group_id = ?, phone = ? WHERE id = ?"
            cursor.execute(update_query, (
                search_params['last_name'],
                search_params['first_name'],
                search_params['patronymic'],
                search_params['birthday_date'],
                search_params['group_id'],
                search_params['phone'],
                id
            ))
            conn.commit()
            archive_query = "INSERT INTO Archive_student (id, last_name, first_name, patronymic, birthday_date, group_id, phone) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(archive_query, (
                old_data['id'],
                old_data['last_name'],
                old_data['first_name'],
                old_data['patronymic'],
                old_data['birthday_date'],
                old_data['group_id'],
                old_data['phone']
            ))
            conn.commit()

        # Redirect the user to the student list page
        return redirect(url_for('studentsList'))

    conn.close()

    return render_template('edit-student.html', data=data_cursor)


@app.route('/file')
def show_file():
    # Get the name of the file to download from the query string parameter
    filename = request.args.get('filename')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Retrieve the file data from SQLite
    query = "SELECT file FROM Files WHERE file_name = ?"
    cursor.execute(query, (filename,))
    file_data = cursor.fetchone()

    conn.close()

    if file_data:
        file_data = file_data[0]  # Encode as bytes
        contents = BytesIO(file_data)

        # Set the Content-Type header based on file extension
        content_type = mimetypes.guess_type(filename)[0]
        if not content_type:
            content_type = 'application/octet-stream'

        response = make_response(contents.getvalue())
        response.headers.set('Content-Type', content_type)

        # Set the Content-Disposition header to "attachment" for non-PDF files
        if content_type != 'application/pdf':
            filename_header = 'filename="%s"' % urllib.parse.quote(filename.encode('utf-8'))
            response.headers.set('Content-Disposition', 'attachment', filename=filename_header)
        else:
            filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(filename.encode('utf-8'))
            response.headers.set('Content-Disposition', 'inline', filename=filename_header)

        return response
    else:
        return "File not found."

@app.route('/teachers', methods=['GET', 'POST'])
def teachers():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # query = 'SELECT chair_code FROM groups WHERE _id = ?'
    # group_id = session.get('group_id')
    # cursor.execute(query, (group_id,))
    # group_data = cursor.fetchone()
    group_ids = session['group_ids']

    query = """
        SELECT * FROM Lecturer l
        WHERE l.id IN (
            SELECT lecturer_id
            FROM LecturerGroup
            WHERE group_id in ({})
        )
        """.format(','.join('?' for _ in group_ids))
    cursor.execute(query, group_ids)

    # Get the column names
    column_names = [description[0] for description in cursor.description]

    # Fetch the results
    lecturer_data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    if request.method == 'GET':
        search_params = {}

        # Extract query parameters and update search_params dictionary
        search_params['id'] = request.args.get('id', default='', type=str)
        search_params['surname'] = request.args.get('surname', default='', type=str)
        search_params['phone'] = request.args.get('phone', default='', type=str)

        # Filter lecturer_data based on search_params
        if search_params['id']:
            lecturer_data = [data for data in lecturer_data if search_params['id'] in data['_id']]
        if search_params['surname']:
            lecturer_data = [data for data in lecturer_data if search_params['surname'].lower() == data['surname'].lower()]
        if search_params['phone']:
            lecturer_data = [data for data in lecturer_data if search_params['phone'] in data['phone']]

    if request.method == 'POST' and request.form['action'] == 'Download':
        # Create a new Excel workbook and sheet
        wb = Workbook()
        sheet = wb.active

        # Add column headers to the sheet
        sheet['A1'] = 'ID'
        sheet['B1'] = 'Name'
        sheet['C1'] = 'Surname'
        sheet['D1'] = 'Email'
        sheet['E1'] = 'Degree'

        # Add data to the sheet
        for i, data in enumerate(lecturer_data, start=2):
            sheet.cell(row=i, column=1, value=data[0])
            sheet.cell(row=i, column=2, value=data[1])
            sheet.cell(row=i, column=3, value=data[2])
            sheet.cell(row=i, column=4, value=data[3])
            sheet.cell(row=i, column=5, value=data[4])

        # Create a bytes buffer to save the workbook to
        buffer = BytesIO()

        # Save the workbook to the buffer
        wb.save(buffer)

        # Set the buffer's seek pointer to the beginning
        buffer.seek(0)

        # Create a response object with the workbook as the content and headers to trigger a file download
        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = 'attachment; filename=teachers.xlsx'

        conn.close()
        return response

    conn.close()
    return render_template('teachers.html', data=lecturer_data)

@app.route('/subjects', methods=['GET', 'POST'])
def subjects():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    conn2 = sqlite3.connect(DATABASE2)
    cursor2 = conn2.cursor()

    query2 = """
    SELECT s.subject_id, s.subject_name
    FROM Subject s
    WHERE s.subject_id IN (
         SELECT slg.subject_id
         FROM SubjectLecturerGroup slg
         WHERE slg.lecturer_id IN (
              SELECT lecturer_id
              FROM Lecturer
              WHERE lecturer_id IN (
                   SELECT lecturer_id
                   FROM SubjectLecturerGroup
                   WHERE group_id in (?)
              )
         )
    );
    """

    cursor2.execute(query2, session['group_ids'])
    column_names2 = [description[0] for description in cursor2.description]
    subject_data = [dict(zip(column_names2, row)) for row in cursor2.fetchall()]
    print(session['group_ids'])
    data = []
    for subject in subject_data:
        subject_id = subject['subject_id']
        query = "SELECT * FROM Files WHERE subject_id = ?"
        cursor.execute(query, (subject_id,))
        column_names = [description[0] for description in cursor.description]
        files = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        file_data = [{
            'file_name': file['file_name'],
            'file_type': os.path.splitext(file['file_name'])[1]
        } for file in files]
        subject_data = {
            'subject_name': subject['subject_name'],
            'files': file_data
        }
        data.append(subject_data)

    cursor.close()
    conn.close()
    cursor2.close()
    conn2.close()

    return render_template('subjects.html', file_data=  data)


@app.route('/add-subject', methods=['GET', 'POST'])
def addSubjects():
    if request.method == 'POST':
        end_time = int(request.form['end_time'])
        group_name = request.form['group_name']
        messenge = request.form['messenge']
        subject_name = request.form['subject_name']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        expiry_time = datetime.now() + timedelta(seconds=end_time)
        datas = (expiry_time, group_name, messenge, subject_name)
        query = "INSERT INTO Subject (expiry_time, group_name, messenge, subject_name) VALUES (?, ?, ?, ?)"
        cursor.execute(query, datas)
        conn.commit()
        conn.close()

    else :
        return render_template('add-subject.html')
    # form = AddSubjectForm()
    # if form.validate_on_submit():
    #     # Get form data
    #     file = request.files['file']
    #     file_data = file.read()

    #     # create a binary object from the file data
    #     binary_data = bson.binary.Binary(file_data)

    #     first_name = request.form['first_name']
    #     group = request.form['group']

    #     # Store data in MongoDB
    #     document =  {
    #         'first_name': first_name,
    #         'group_id': int(group),
    #         'file_name': file.filename,
    #         'file':binary_data
    #     }
    #     # Save data to MongoDB
    #     files.insert_one(document)

    #     flash('Subject added successfully!', 'success')
    #     time.sleep(5) # Delay for 2 seconds
    #     # return redirect(url_for('dashboard'))

    # # Check if form has been submitted and all fields are not filled
    # if request.method == 'POST' and not form.validate():
    #     flash('Please fill out all fields.', 'danger')

    # messages = get_flashed_messages()
    # if messages:
    #     return render_template('add-subject.html', form=form, messages=messages)

    #     # # Check file size
    #     # file = request.files['file']
    #     # file_size = len(file.read())
    #     # if file_size > 10485760:  # 10 MB in bytes
    #     #     return render_template('add-subject.html', error='File size exceeds the limit')
    #     # filename = file.filename
    #     # print(filename, file_size)
    return render_template('add-subject.html')

@app.route("/exercises", methods=['POST', 'GET'])
def exercie():
    # group_ids = session['group_ids']
    group_ids = (1, )
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = """
        SELECT
            group_name,
            expiry_time,
            subject_name,
            messenge,
            file_name
        FROM Exercises
        WHERE group_id in ({})
    """.format(','.join('?' for _ in group_ids))
    cursor.execute(query, group_ids)
    # Get the column names
    column_names = [description[0] for description in cursor.description]

    # Fetch the results
    exercise_data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    exercise_data = [{
        'group_name': data['group_name'],
        'expiry_time': data['expiry_time'],
        'subject_name': data['subject_name'],
        'messenge': data['messenge'],
        'file_name': data['file_name'],
        'file_type': os.path.splitext(data['file_name'])[1]
    } for data in exercise_data]
    return render_template('exercises.html', data=exercise_data)

@app.route('/add-exercise', methods=['GET', 'POST'])
def addExercise():
    if request.method == 'POST':
        end_time = int(request.form['end_time'])
        group_name = request.form['group_name']
        messenge = request.form['messenge']
        subject_name = request.form['subject_name']
        file = request.files['file'].read()
        file_name = request.files['file'].filename
        group_id = 1

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        subject_id_query = "SELECT subject_id FROM Subject WHERE subject_name = ?"
        cursor.execute(subject_id_query, (subject_name, ))
        subject_id = cursor.fetchone()[0]

        # Check if the record already exists
        check_query = "SELECT COUNT(*) FROM Files WHERE subject_id = ? AND file_name = ?"
        cursor.execute(check_query, (subject_id, file_name))
        record_exists = cursor.fetchone()[0]
        if not record_exists:
            add_file_query = "INSERT OR IGNORE INTO Files (subject_id, file, file_name) VALUES (?, ?, ?)"
            cursor.execute(add_file_query, (subject_id, file, file_name))

        expiry_time = datetime.now() + timedelta(seconds=end_time)
        datas = (expiry_time, group_name, messenge, subject_name, file_name, group_id)
        query = "INSERT INTO Exercises (expiry_time, group_name, messenge, subject_name, file_name, group_id) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, datas)
        conn.commit()
        conn.close()

    else :
        return render_template('add-exercise.html')

    return render_template('add-exercise.html')

# # Background task to check and delete expired rows
# def delete_expired_rows():
#     # with app.app_context():
#     # Connect to the SQLite database
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()

#     current_time = datetime.now()
#     query = "DELETE FROM Exercises WHERE expiry_time <= ?"
#     cursor.execute(query, (current_time,))
#     conn.commit()
#     print("Expired values deleted.")
#     conn.commit()
#     conn.close()


if __name__ == '__main__':
    app.run()