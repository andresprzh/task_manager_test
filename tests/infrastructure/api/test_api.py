import uuid

from fastapi import FastAPI
from fastapi.testclient import TestClient
from task_manager.application.security.jwt import create_access_token

from task_manager.infrastructure.api.task import get_list_router, get_task_router


def test_list_endpoints_crud(fake_list_usecases):
    """Test the CRUD operations of the list endpoints using a
    fake in-memory use case implementation."""

    router = get_list_router(fake_list_usecases)
    app = FastAPI()
    app.include_router(router)

    client = TestClient(app)
    token = create_access_token({"sub": "testuser"})
    headers = {"Authorization": f"Bearer {token}"}

    # create
    resp = client.post(
        "/lists/", json={"name": "L1", "description": "d"}, headers=headers
    )
    assert resp.status_code == 201
    body = resp.json()
    list_id = body["id"]

    # list
    resp = client.get("/lists/", headers=headers)
    assert resp.status_code == 200
    assert any(element["id"] == list_id for element in resp.json())

    # get
    resp = client.get(f"/lists/{list_id}", headers=headers)
    assert resp.status_code == 200

    # update
    resp = client.put(
        f"/lists/{list_id}", json={"name": "L2", "description": None}, headers=headers
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "L2"

    # delete
    resp = client.delete(f"/lists/{list_id}", headers=headers)
    assert resp.status_code == 204

    # get missing -> 404
    resp = client.get(f"/lists/{list_id}", headers=headers)
    assert resp.status_code == 404


def test_task_endpoints_crud_and_status(fake_task_usecases):
    """Test the CRUD operations of the task endpoints and status
    updates using a fake in-memory use case implementation."""

    # create a list id to reference
    list_id = uuid.uuid4()

    router = get_task_router(fake_task_usecases)
    app = FastAPI()
    app.include_router(router)

    client = TestClient(app)
    token = create_access_token({"sub": "testuser"})
    headers = {"Authorization": f"Bearer {token}"}

    # create
    payload = {
        "title": "T1",
        "list_id": str(list_id),
        "description": "d",
        "status": "pending",
        "priority": "medium",
    }
    resp = client.post("/tasks/", json=payload, headers=headers)
    assert resp.status_code == 201
    tid = resp.json()["id"]

    # get
    resp = client.get(f"/tasks/{tid}", headers=headers)
    assert resp.status_code == 200

    # update status
    resp = client.patch(f"/tasks/{tid}", json={"status": "completed"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"

    # update full
    resp = client.put(
        f"/tasks/{tid}",
        json={
            "title": "T2",
            "list_id": str(list_id),
            "description": "now",
            "status": "in_progress",
            "priority": "high",
        },
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "T2"

    # delete
    resp = client.delete(f"/tasks/{tid}", headers=headers)
    assert resp.status_code == 204

    # get missing -> 404
    resp = client.get(f"/tasks/{tid}", headers=headers)
    assert resp.status_code == 404
