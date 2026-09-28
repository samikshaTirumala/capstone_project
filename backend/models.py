from pydantic import BaseModel, Field, StrictBool, field_validator


class StudentPerformance(BaseModel):
    """Canonical schema shared by the API and client."""

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
