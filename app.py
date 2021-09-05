from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Resident, ResidentCreate, ResidentRead, ResidentUpdate

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/residents/", response_model=ResidentRead)
def create_resident(
    *, session: Session = Depends(get_session), resident: ResidentCreate
):
    db_resident = Resident.from_orm(resident)
    session.add(db_resident)
    session.commit()
    session.refresh(db_resident)
    return db_resident


@app.get("/residents/", response_model=List[ResidentRead])
def read_residents(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=300, lte=300),
):
    residents = session.exec(select(Resident).offset(offset).limit(limit)).all()
    return residents


@app.get("/residents/{resident_id}", response_model=ResidentRead)
def read_resident(*, session: Session = Depends(get_session), resident_id: int):
    resident = session.get(Resident, resident_id)
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    return resident


@app.patch("/residents/{resident_id}", response_model=ResidentRead)
def update_resident(
    *,
    session: Session = Depends(get_session),
    resident_id: int,
    resident: ResidentUpdate,
):
    db_resident = session.get(Resident, resident_id)
    if not db_resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    resident_data = resident.dict(exclude_unset=True)
    for key, value in resident_data.items():
        setattr(db_resident, key, value)
    session.add(db_resident)
    session.commit()
    session.refresh(db_resident)
    return db_resident


@app.delete("/residents/{resident_id}")
def delete_resident(*, session: Session = Depends(get_session), resident_id: int):

    resident = session.get(Resident, resident_id)
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    session.delete(resident)
    session.commit()
    return {"ok": True}


# def main():
#     create_db_and_tables()
#
# if __name__ == "__main__":
#     main()
#
#     response = client.post("/residents/", json={"name": name, "hometown": hometown})
#     data = response.json()
