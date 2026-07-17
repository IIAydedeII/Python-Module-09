#!/usr/bin/env python3
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(Enum):
    """Crew member ranks."""

    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    """Individual member of a crew."""

    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)

    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.rank.value}) - {self.specialization}"


class SpaceMission(BaseModel):
    """Assigned mission for a given crew"""

    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)

    launch_date: datetime
    duration_days: int = Field(ge=1, le=365 * 10)

    crew: list[CrewMember] = Field(min_length=1, max_length=12)

    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10_000.0)

    @model_validator(mode="after")
    def custom_validator(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        ranks = [member.rank for member in self.crew]
        if Rank.commander not in ranks and Rank.captain not in ranks:
            raise ValueError("Must have at least one Commander or Captain")

        if self.duration_days > 365:
            experienced = [
                member for member in self.crew if member.years_experience >= 5
            ]
            if len(experienced) < len(self.crew) / 2:
                raise ValueError(
                    "Long missions (> 365 days) "
                    "need 50%% experienced crew (5+ years)"
                )

        for member in self.crew:
            if not member.is_active:
                raise ValueError("All crew members must be active")

        return self

    def __str__(self) -> str:
        duration = "day" if self.duration_days == 1 else "days"
        return "\n".join(
            [
                f"Mission: {self.mission_name}",
                f"ID: {self.mission_id}",
                f"Destination: {self.destination}",
                f"Duration: {self.duration_days} {duration}",
                f"Budget: ${self.budget_millions}M",
                f"Crew size: {len(self.crew)}",
                "Crew members:",
                *[f"- {member}" for member in self.crew],
            ]
        )


def main() -> None:
    print("Space Mission Crew Validation")

    print("=========================================")
    print("Valid mission created:")
    print(
        SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="SC001",
                    name="Sarah Conor",
                    rank=Rank.commander,
                    age=42,
                    specialization="Mission Command",
                    years_experience=8,
                ),
                CrewMember(
                    member_id="JS045",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    age=24,
                    specialization="Navigation",
                    years_experience=4,
                ),
                CrewMember(
                    member_id="AJ010",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    age=27,
                    specialization="Engineering",
                    years_experience=5,
                ),
            ],
        )
    )

    print()
    print("=========================================")
    print("Expected validation error:")
    try:
        print(
            SpaceMission(
                mission_id="M2024_MARS",
                mission_name="Mars Colony Establishment",
                destination="Mars",
                launch_date=datetime.now(),
                duration_days=900,
                budget_millions=2500.0,
                crew=[
                    CrewMember(
                        member_id="SC001",
                        name="Sarah Conor",
                        rank=Rank.cadet,
                        age=42,
                        specialization="Mission Command",
                        years_experience=8,
                    ),
                    CrewMember(
                        member_id="JS045",
                        name="John Smith",
                        rank=Rank.lieutenant,
                        age=24,
                        specialization="Navigation",
                        years_experience=4,
                    ),
                    CrewMember(
                        member_id="AJ010",
                        name="Alice Johnson",
                        rank=Rank.officer,
                        age=27,
                        specialization="Engineering",
                        years_experience=5,
                    ),
                ],
            )
        )
    except ValidationError as e:
        for error in e.errors():
            print(error.get("msg"))


if __name__ == "__main__":
    main()
