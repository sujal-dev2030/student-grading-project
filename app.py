
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


def main():
    name = input("Student name: ")
    department = input("Department: ")
    semester = input("Semester: ")

    marks = []
    for subject in range(1, 4):
        mark = float(input(f"Marks for subject {subject}: "))
        marks.append(mark)

    average = calculate_average(marks)
    grade = calculate_grade(average)

    print("\n--- Student Result ---")
    print(f"Name: {name}")
    print(f"Department: {department}")
    print(f"Semester: {semester}")
    print(f"Average: {average:.2f}")
    print(f"Grade: {grade}")


if __name__ == "__main__":
    main()
