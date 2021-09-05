from __future__ import annotations

from sqlmodel import Field, SQLModel


class ResidentBase(SQLModel):
    name: str
    category: str | None
    hometown: str
    college: str | None
    medicalschool: str | None
    careerplans: str | None
    bio: str | None
    img: str | None
    popup: str | None
    hometownlatitude: float | None
    hometownlongitude: float | None
    collegelatitude: float | None
    collegelongitude: float | None
    medschoollatitude: float | None
    medschoollongitude: float | None


class Resident(ResidentBase, table=True):
    name: str = Field(primary_key=True)


class ResidentRead(ResidentBase):
    name: str


class ResidentCreate(ResidentBase):
    pass


class ResidentUpdate(SQLModel):
    name: str | None
    category: str | None
    hometown: str | None
    college: str | None
    medicalschool: str | None
    careerplans: str | None
    bio: str | None
    img: str | None
    popup: str | None
    hometownlatitude: float | None
    hometownlongitude: float | None
    collegelatitude: float | None
    collegelongitude: float | None
    medschoollatitude: float | None
    medschoollongitude: float | None
