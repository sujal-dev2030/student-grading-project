import pytest
from app import app, calculate_average, calculate_grade


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.mark.parametrize(
    ("average", "expected"),
    [
        (95, "S"),
        (85, "A"),
        (70, "B"),
        (55, "C"),
        (45, "D"),
        (30, "F"),
    ],
)
def test_calculate_grade(average, expected):
    assert calculate_grade(average) == expected


def test_calculate_average():
    assert calculate_average([90, 80, 100]) == pytest.approx(90)


def test_reject_wrong_number_of_marks():
    with pytest.raises(ValueError):
        calculate_average([90, 80])


def test_reject_out_of_range_marks():
    with pytest.raises(ValueError):
        calculate_average([90, 80, 101])


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Grading System" in response.data


def test_submit_student_result(client):
    response = client.post(
        "/",
        data={
            "name": "Rahul",
            "department": "CSE",
            "semester": "5",
            "mark1": "90",
            "mark2": "85",
            "mark3": "95",
        },
    )
    assert response.status_code == 200
    assert b"Rahul" in response.data
    assert b"90.00" in response.data
    assert b"Grade:</strong>" in response.data
    assert b">S</span>" in response.data


def test_reject_invalid_marks(client):
    response = client.post(
        "/",
        data={
            "name": "Rahul",
            "department": "CSE",
            "semester": "5",
            "mark1": "90",
            "mark2": "85",
            "mark3": "150",
        },
    )
    assert response.status_code == 200
    assert b"Enter valid details." in response.data
