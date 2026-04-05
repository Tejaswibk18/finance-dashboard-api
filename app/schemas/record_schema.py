from pydantic import BaseModel, Field, field_validator
from datetime import datetime , timezone
from typing import Optional
import re


class RecordCreate(BaseModel):
    amount: float = Field(gt=0)
    type: str
    category: str
    date: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = None

    @field_validator("type", "category")
    @classmethod
    def validate_text_fields(cls, value: str, info):

        field_name = info.field_name  # type / category

        if not value or not value.strip():
            raise ValueError(f"{field_name} should not be empty")

        pattern = r"^[a-zA-Z_-]+$"
        if not re.match(pattern, value):
            raise ValueError(
                f"{field_name} must contain only alphabets, underscore or hyphen"
            )

        return value.lower()


class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[str]
    category: Optional[str]
    date: Optional[datetime]
    notes: Optional[str]

    @field_validator("type", "category")
    @classmethod
    def validate_text_fields(cls, value):
        if value is None:
            return value

        pattern = r"^[a-zA-Z_-]+$"
        if not re.match(pattern, value):
            raise ValueError(
                "Only alphabets, underscore and hyphen allowed"
            )
        return value.lower()