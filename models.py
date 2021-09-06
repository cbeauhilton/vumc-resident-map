from __future__ import annotations

from typing import Optional

from sqlmodel import VARCHAR, Column, Field, SQLModel


class ResidentBase(SQLModel):
    name: str = Field(sa_column=Column("name", VARCHAR, unique=True))
    hometown: Optional[str] = None
    category: Optional[str] = None
    college: Optional[str] = None
    medicalschool: Optional[str] = None
    careerplans: Optional[str] = None
    bio: Optional[str] = None
    img: Optional[str] = None
    popup: Optional[str] = None
    hometownlatitude: Optional[float] = None
    hometownlongitude: Optional[float] = None
    collegelatitude: Optional[float] = None
    collegelongitude: Optional[float] = None
    medschoollatitude: Optional[float] = None
    medschoollongitude: Optional[float] = None


class Resident(ResidentBase, table=True):
    id: int = Field(default=None, primary_key=True)


class ResidentRead(ResidentBase):
    id: int


class ResidentCreate(ResidentBase):
    pass


class ResidentUpdate(SQLModel):
    name: Optional[str] = None
    hometown: Optional[str] = None
    category: Optional[str] = None
    college: Optional[str] = None
    medicalschool: Optional[str] = None
    careerplans: Optional[str] = None
    bio: Optional[str] = None
    img: Optional[str] = None
    popup: Optional[str] = None
    hometownlatitude: Optional[float] = None
    hometownlongitude: Optional[float] = None
    collegelatitude: Optional[float] = None
    collegelongitude: Optional[float] = None
    medschoollatitude: Optional[float] = None
    medschoollongitude: Optional[float] = None
