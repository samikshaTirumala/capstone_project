from pathlib import Path

import pandas as pd

from .models import StudentPerformance


CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "students_cleaned.csv"


def get_all_students() -> list[StudentPerformance]:
    dataframe = pd.read_csv(CSV_PATH)
    return [StudentPerformance.model_validate(record) for record in dataframe.to_dict(orient="records")]


def find_student(student_id: str) -> list[StudentPerformance]:
    return [student for student in get_all_students() if student.student_id == student_id]


def calculate_average_score() -> float:
    dataframe = pd.read_csv(CSV_PATH)
    return round(float(dataframe["score"].mean()), 2)


def calculate_average_attendance() -> float:
    dataframe = pd.read_csv(CSV_PATH)
    return round(float(dataframe["attendance"].mean()), 2)


def calculate_pass_percentage() -> float:
    dataframe = pd.read_csv(CSV_PATH)
    return round(float(dataframe["passed"].mean() * 100), 2)


def calculate_subject_wise_average_score() -> dict[str, float]:
    dataframe = pd.read_csv(CSV_PATH)
    averages = dataframe.groupby("subject")["score"].mean().round(2)
    return {subject: float(average) for subject, average in averages.items()}
