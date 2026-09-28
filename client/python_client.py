import sys

import requests
from pydantic import BaseModel, Field, StrictBool, TypeAdapter, field_validator


class StudentPerformance(BaseModel):
    student_id: str = Field(min_length=1)
    student_name: str = Field(min_length=1)
    subject: str = Field(min_length=1)
    score: float = Field(ge=0, le=100)
    attendance: float = Field(ge=0, le=100)
    passed: StrictBool

    @field_validator("student_id", "student_name", "subject")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("text fields cannot be blank")
        return value


class AnalyticsSummary(BaseModel):
    total_records: int = Field(ge=0)
    average_score: float = Field(ge=0, le=100)
    average_attendance: float = Field(ge=0, le=100)
    pass_percentage: float = Field(ge=0, le=100)
    subject_wise_average_score: dict[str, float]


class AnalyticsClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000") -> None:
        self.base_url = base_url.rstrip("/")
        self._students_adapter = TypeAdapter(list[StudentPerformance])

    def get_students(self) -> list[StudentPerformance]:
        response = self._get("/students")
        response.raise_for_status()
        return self._students_adapter.validate_python(response.json())

    def get_student(self, student_id: str) -> list[StudentPerformance]:
        response = self._get(f"/students/{student_id}")
        response.raise_for_status()
        return self._students_adapter.validate_python(response.json())

    def get_analytics(self) -> AnalyticsSummary:
        response = self._get("/analytics")
        response.raise_for_status()
        return AnalyticsSummary.model_validate(response.json())

    def _get(self, path: str) -> requests.Response:
        try:
            return requests.get(f"{self.base_url}{path}", timeout=10)
        except requests.exceptions.ConnectionError as error:
            raise RuntimeError(
                "Cannot connect to the API. Start it first with "
                "python -m uvicorn backend.main:app --reload"
            ) from error


def main() -> None:
    client = AnalyticsClient()
    students = client.get_students()
    analytics = client.get_analytics()

    print(f"Loaded {len(students)} typed student records")
    print(f"Average score: {analytics.average_score}")
    print(f"Average attendance: {analytics.average_attendance}")
    print(f"Pass percentage: {analytics.pass_percentage}")

    first_student = client.get_student(students[0].student_id)
    print(f"{students[0].student_id} has {len(first_student)} subject records")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error)
        sys.exit(1)
