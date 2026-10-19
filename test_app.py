
import pytest
from app import calculate_average, calculate_grade


@pytest.mark.parametrize(
    "average, expected",
    [
        (95, "S"),
        (85, "A"),
        (70, "B"),
        (55, "C"),
        (45, "D"),
        (30, "F"),
        (89.5, "A"),
    ],
)
def test_grade_boundaries(average, expected):
    assert calculate_grade(average) == expected


def test_average():
    assert calculate_average([90, 80, 70]) == 80


def test_rejects_invalid_marks():
    with pytest.raises(ValueError):
        calculate_average([90, 110, 70])


def test_requires_three_marks():
    with pytest.raises(ValueError):
        calculate_average([90, 80])
