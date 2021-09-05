import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app import app
from database import get_session
from models import Resident


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

    name = "Deadpond"
    hometown = "Paris, TX"

    response = client.post("/residents/", json={"name": name, "hometown": hometown})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpond"
    assert data["hometown"] == "Paris, TX"
    assert data["careerplans"] is None
    assert data["id"] is not None


def test_create_resident_incomplete(client: TestClient):
    # No hometown
    response = client.post("/residents/", json={"hometown": "Mars"})
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
    names = ["Deadpond", "Rusty-Man", "Beau Hilton"]
    hometowns = ["NY, NY", "Bali", "Glendale, Arizona"]
    categories = [None, None, "PGY1"]
    resident_0 = Resident(name=names[0], hometown=hometowns[0])
    resident_1 = Resident(name=names[1], hometown=hometowns[1])
    resident_2 = Resident(name=names[2], hometown=hometowns[2], category=categories[2])
    session.add(resident_0)
    session.add(resident_1)
    session.add(resident_2)
    session.commit()

    response = client.get("/residents/")
    data = response.json()
    print(data)

    assert response.status_code == 200

    assert len(data) == 3
    assert data[0]["name"] == resident_0.name
    assert data[0]["hometown"] == resident_0.hometown
    assert data[0]["category"] == resident_0.category
    assert data[0]["careerplans"] == resident_0.careerplans
    assert data[1]["name"] == resident_1.name
    assert data[1]["hometown"] == resident_1.hometown
    assert data[1]["college"] == resident_1.college
    assert data[2]["id"] == resident_2.id


def test_read_resident(session: Session, client: TestClient):
    resident_1 = Resident(
        name="Deadpond",
        hometown="Dive Wilson",
        bio="I like to do drawings.",
        careerplans="hemapofery tomfoolery",
    )
    session.add(resident_1)
    session.commit()

    response = client.get(f"/residents/{resident_1.id}")
    data = response.json()
    print(data)

    assert response.status_code == 200
    assert data["name"] == resident_1.name
    assert data["hometown"] == resident_1.hometown
    assert data["careerplans"] == resident_1.careerplans
    assert data["bio"] == resident_1.bio


def test_update_resident(session: Session, client: TestClient):
    resident_1 = Resident(name="Deadpond", hometown="Dive Wilson")
    session.add(resident_1)
    session.commit()

    response = client.patch(f"/residents/{resident_1.id}", json={"name": "Deadpuddle"})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpuddle"
    assert data["hometown"] == "Dive Wilson"
    assert data["college"] is None


def test_delete_resident(session: Session, client: TestClient):
    resident_1 = Resident(name="Deadpond", hometown="Dive Wilson")
    session.add(resident_1)
    session.commit()

    response = client.delete(f"/residents/{resident_1.id}")

    resident_in_db = session.get(Resident, resident_1.id)

    assert response.status_code == 200

    assert resident_in_db is None
