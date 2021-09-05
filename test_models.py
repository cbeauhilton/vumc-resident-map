import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from .app import app
from .database import get_session
from .models import Resident


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_resident(client: TestClient):
    response = client.post(
        "/residents/", json={"name": "Deadpond", "hometown": "Dive Wilson"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpond"
    assert data["hometown"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] is not None


def test_create_resident_incomplete(client: TestClient):
    # No hometown
    response = client.post("/residents/", json={"name": "Deadpond"})
    assert response.status_code == 422


def test_create_resident_invalid(client: TestClient):
    # hometown has an invalid type
    response = client.post(
        "/residents/",
        json={
            "name": "Deadpond",
            "hometown": {"message": "Do you wanna know my secret identity?"},
        },
    )
    assert response.status_code == 422


def test_read_residents(session: Session, client: TestClient):
    resident_1 = Resident(name="Deadpond", hometown="NY, NY")
    resident_2 = Resident(name="Rusty-Man", hometown="Tommy Sharp")
    resident_3 = Resident(
        name="Beau",
        category="PGY1",
        hometown="Glendale, Arizona",
    )
    session.add(resident_1)
    session.add(resident_2)
    session.add(resident_3)
    session.commit()

    response = client.get("/residents/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["name"] == resident_1.name
    assert data[0]["hometown"] == resident_1.hometown
    assert data[0]["category"] == resident_1.category
    assert data[0]["careerplans"] == resident_1.careerplans
    assert data[1]["name"] == resident_2.name
    assert data[1]["hometown"] == resident_2.hometown
    assert data[1]["college"] == resident_2.college
    assert data[2]["category"] == resident_3.category


def test_read_resident(session: Session, client: TestClient):
    resident_1 = Resident(
        name="Deadpond",
        hometown="Dive Wilson",
        bio="I like to do drawings.",
        careerplans="hemapofery tomfoolery",
    )
    session.add(resident_1)
    session.commit()

    response = client.get(f"/residents/{resident_1.name}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == resident_1.name
    assert data["hometown"] == resident_1.hometown
    assert data["careerplans"] == resident_1.careerplans
    assert data["bio"] == resident_1.bio


def test_update_resident(session: Session, client: TestClient):
    resident_1 = Resident(name="Deadpond", hometown="Dive Wilson")
    session.add(resident_1)
    session.commit()

    response = client.patch(
        f"/residents/{resident_1.name}", json={"name": "Deadpuddle"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpuddle"
    assert data["hometown"] == "Dive Wilson"
    assert data["college"] is None


def test_delete_resident(session: Session, client: TestClient):
    resident_1 = Resident(name="Deadpond", hometown="Dive Wilson")
    session.add(resident_1)
    session.commit()

    response = client.delete(f"/residents/{resident_1.name}")

    resident_in_db = session.get(Resident, resident_1.name)

    assert response.status_code == 200

    assert resident_in_db is None
