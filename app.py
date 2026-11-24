
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd
from database import create_database

app = Flask(__name__)

# Create database
create_database()


# Connect to database
def get_connection():
    return sqlite3.connect("students.db")


# Calculate grade
def calculate_grade(percentage):

    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


# Dashboard page
@app.route("/")
def dashboard():

    conn = get_connection()

    students = pd.read_sql_query("SELECT * FROM students", conn)

    total_students = len(students)

    if total_students > 0:
        average = round(students["percentage"].mean(), 2)
        highest = students["percentage"].max()
        passed = len(students[students["result"] == "Pass"])
        pass_percentage = round((passed / total_students) * 100, 2)
    else:
        average = 0
        highest = 0
        pass_percentage = 0

    conn.close()

    return render_template(
        "index.html",
        total_students=total_students,
        average=average,
        highest=highest,
        pass_percentage=pass_percentage
    )


# Add student page
@app.route("/add-student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        roll = request.form["roll_number"]

        english = int(request.form["english"])
        python = int(request.form["python"])
        maths = int(request.form["maths"])
        dbms = int(request.form["dbms"])
        java = int(request.form["java"])

        marks = [english, python, maths, dbms, java]

        total = sum(marks)
        percentage = round(total / 5, 2)

        grade = calculate_grade(percentage)

        if all(mark >= 40 for mark in marks):
            result = "Pass"
        else:
            result = "Fail"

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students
            (name, roll_number, english, python, maths,
            dbms, java, total, percentage, grade, result)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, roll, english, python, maths,
              dbms, java, total, percentage, grade, result))

        conn.commit()
        conn.close()

        return redirect(url_for("records"))

    return render_template("add_student.html")


# Student records page
@app.route("/records")
def records():

    conn = get_connection()

    students = pd.read_sql_query(
        "SELECT * FROM students ORDER BY id DESC", conn
    )

    conn.close()

    return render_template(
        "records.html",
        students=students.to_dict(orient="records")
    )


# Delete student
@app.route("/delete/<int:id>")
def delete_student(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("records"))


# Analytics page
@app.route("/analytics")
def analytics():

    conn = get_connection()

    students = pd.read_sql_query("SELECT * FROM students", conn)

    if len(students) > 0:

        subjects = ["english", "python", "maths", "dbms", "java"]

        subject_averages = [
            round(students[subject].mean(), 2)
            for subject in subjects
        ]

        grade_counts = students["grade"].value_counts().to_dict()

        student_names = students["name"].tolist()
        student_percentages = students["percentage"].tolist()

    else:

        subjects = ["english", "python", "maths", "dbms", "java"]
        subject_averages = [0, 0, 0, 0, 0]
        grade_counts = {}
        student_names = []
        student_percentages = []

    conn.close()

    return render_template(
        "analytics.html",
        subjects=subjects,
        subject_averages=subject_averages,
        grade_counts=grade_counts,
        student_names=student_names,
        student_percentages=student_percentages
    )


if __name__ == "__main__":
    app.run(debug=True)
