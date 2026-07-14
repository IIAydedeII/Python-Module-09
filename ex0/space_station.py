#!/usr/bin/env python3
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    """Validated vital statistics for a space station."""

    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)

    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)

    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None, max_length=200)

    def __str__(self) -> str:
        subject = "person" if self.crew_size == 1 else "people"
        status = "Operational" if self.is_operational else "Non-operational"
        return "\n".join(
            [
                f"ID: {self.station_id}",
                f"Name: {self.name}",
                f"Crew: {self.crew_size} {subject}",
                f"Power: {self.power_level:.1f}%",
                f"Oxygen: {self.oxygen_level:.1f}%",
                f"Status: {status}",
            ]
        )


def main() -> None:
    print("Space Station Data Validation")

    print("========================================")
    print("Valid station created:")
    print(
        SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2000, 11, 2),
        )
    )

    print()
    print("========================================")
    print("Expected validation error:")
    try:
        print(
            SpaceStation(
                station_id="ISS001",
                name="International Space Station",
                crew_size=21,
                power_level=85.5,
                oxygen_level=92.3,
                last_maintenance=datetime(2000, 11, 2),
            )
        )
    except ValidationError as e:
        for error in e.errors():
            print(error.get("msg"))


if __name__ == "__main__":
    main()
