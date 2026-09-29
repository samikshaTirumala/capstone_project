from fastapi import FastAPI, HTTPException

from analytics import (
    calculate_average_attendance,
    calculate_average_score,
    calculate_pass_percentage,
    calculate_subject_wise_average_score,
    find_student,
    get_all_students,
)

from models import AnalyticsSummary, StudentPerformance


app = FastAPI(title="Student Performance Analytics API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Student performance analytics API is running"}


@app.get("/students", response_model=list[StudentPerformance])
def read_students() -> list[StudentPerformance]:
    return get_all_students()


@app.get("/students/{student_id}", response_model=list[StudentPerformance])
def read_student(student_id: str) -> list[StudentPerformance]:
    students = find_student(student_id)
    if not students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students


@app.get("/analytics", response_model=AnalyticsSummary)
def read_analytics() -> AnalyticsSummary:
    students = get_all_students()
    return AnalyticsSummary(
        total_records=len(students),
        average_score=calculate_average_score(),
        average_attendance=calculate_average_attendance(),
        pass_percentage=calculate_pass_percentage(),
        subject_wise_average_score=calculate_subject_wise_average_score(),
    )
