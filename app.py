from flask import Flask, request, render_template_string

app = Flask(__name__)


def calculate_grade(average):
    if 90 <= average <= 100:
        return "S"
    elif average >= 80:
        return "A"
    elif average >= 65:
        return "B"
    elif average >= 50:
        return "C"
    elif average >= 40:
        return "D"
    else:
        return "F"


def calculate_average(marks):
    if len(marks) != 3:
        raise ValueError("Enter marks for exactly 3 subjects.")

    if any(mark < 0 or mark > 100 for mark in marks):
        raise ValueError("Each mark must be between 0 and 100.")

    return sum(marks) / 3


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Student Grading System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef2ff;
            margin: 0;
            padding: 30px 15px;
            color: #172554;
        }
        .card {
            max-width: 520px;
            margin: auto;
            padding: 28px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 28px #17255420;
        }
        h1 { text-align: center; color: #3730a3; }
        label { display: block; margin-top: 14px; font-weight: bold; }
        input {
            box-sizing: border-box;
            width: 100%;
            padding: 11px;
            margin-top: 6px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
        }
        button {
            width: 100%;
            padding: 13px;
            margin-top: 22px;
            background: #4f46e5;
            color: white;
            border: 0;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        .result, .error {
            margin-top: 22px;
            padding: 16px;
            border-radius: 10px;
        }
        .result { background: #ecfdf5; color: #065f46; }
        .error { background: #fef2f2; color: #991b1b; }
        .grade { font-size: 28px; font-weight: bold; }
    </style>
</head>
<body>
    <main class="card">
        <h1>Student Grading System</h1>
        <p>Enter student details and marks for three subjects.</p>

        <form method="post">
            <label for="name">Student name</label>
            <input id="name" name="name" required maxlength="100"
                   value="{{ values.get('name', '') }}">

            <label for="department">Department</label>
            <input id="department" name="department" required maxlength="100"
                   value="{{ values.get('department', '') }}">

            <label for="semester">Semester</label>
            <input id="semester" name="semester" type="number"
                   min="1" max="20" required
                   value="{{ values.get('semester', '') }}">

            {% for i in range(1, 4) %}
            <label for="mark{{ i }}">Subject {{ i }} marks (0–100)</label>
            <input id="mark{{ i }}" name="mark{{ i }}" type="number"
                   min="0" max="100" step="any" required
                   value="{{ values.get('mark' ~ i, '') }}">
            {% endfor %}

            <button type="submit">Calculate Grade</button>
        </form>

        {% if error %}
        <div class="error" role="alert">{{ error }}</div>
        {% endif %}

        {% if result %}
        <section class="result" aria-live="polite">
            <h2>Student Result</h2>
            <p><strong>Name:</strong> {{ result.name }}</p>
            <p><strong>Department:</strong> {{ result.department }}</p>
            <p><strong>Semester:</strong> {{ result.semester }}</p>
            <p><strong>Average:</strong> {{ "%.2f"|format(result.average) }}</p>
            <p><strong>Grade:</strong> <span class="grade">{{ result.grade }}</span></p>
        </section>
        {% endif %}
    </main>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    values = request.form.to_dict() if request.method == "POST" else {}
    result = None
    error = None

    if request.method == "POST":
        try:
            name = values.get("name", "").strip()
            department = values.get("department", "").strip()
            semester = int(values.get("semester", ""))

            if not name or not department:
                raise ValueError("Enter the student name and department.")

            if not 1 <= semester <= 20:
                raise ValueError("Semester must be between 1 and 20.")

            marks = [float(values[f"mark{i}"]) for i in range(1, 4)]
            average = calculate_average(marks)

            result = {
                "name": name,
                "department": department,
                "semester": semester,
                "average": average,
                "grade": calculate_grade(average),
            }
        except (ValueError, KeyError):
            error = "Enter valid details. Each subject mark must be between 0 and 100."

    return render_template_string(
        HTML, values=values, result=result, error=error
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
