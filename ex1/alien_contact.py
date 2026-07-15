#!/usr/bin/env python3
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(Enum):
    """Documented methods of contact"""

    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    """Validated report for a supposed alien contact."""

    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)

    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=60 * 24)
    witness_count: int = Field(ge=1, le=100)

    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def custom_validator(self) -> AlienContact:
        if self.contact_id[:2] != "AC":
            raise ValueError('Contact ID must start with "AC"')

        if self.contact_type is ContactType.physical:
            if not self.is_verified:
                raise ValueError("Physical contact reports must be verified")

        if self.contact_type is ContactType.telepathic:
            if self.witness_count < 3:
                raise ValueError(
                    "Telepathic contact requires at least 3 witnesses"
                )

        if self.signal_strength > 7.0:
            if not self.message_received:
                raise ValueError(
                    "Strong signals (> 7.0) should include received messages"
                )

        return self

    def __str__(self) -> str:
        return "\n".join(
            [
                f"ID: {self.contact_id}",
                f"Type: {self.contact_type.value}",
                f"Location: {self.location}",
                f"Signal: {self.signal_strength}/10",
                f"Duration: {self.duration_minutes} minutes",
                f"Witnesses: {self.witness_count}",
                f"Message: '{self.message_received}'",
            ]
        )


def main() -> None:
    print("Alien Contact Log Validation")

    print("======================================")
    print("Valid contact report:")
    print(
        AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
        )
    )

    print()
    print("======================================")
    print("Expected validation error:")
    try:
        print(
            AlienContact(
                contact_id="AC_2024_001",
                timestamp=datetime.now(),
                location="Area 51, Nevada",
                contact_type=ContactType.telepathic,
                signal_strength=8.5,
                duration_minutes=45,
                witness_count=2,
                message_received="Greetings from Zeta Reticuli",
            )
        )
    except ValidationError as e:
        for error in e.errors():
            print(error.get("msg"))


if __name__ == "__main__":
    main()
