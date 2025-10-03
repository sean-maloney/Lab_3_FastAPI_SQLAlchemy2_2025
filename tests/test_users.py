# tests/test_users.py
import pytest
def user_payload(uid=1, name="Sean", email="sm@atu.ie", age=22, sid="S1234567"):
 return {"user_id": uid, "name": name, "email": email, "age": age, "student_id": sid}

# testing to see if user creates ok
def test_create_user_ok(client):
    r = client.post("/api/users", json=user_payload())
    assert r.status_code == 201
    data = r.json()
    assert data["user_id"] == 1
    assert data["name"] == "Sean"

# testing for duplicate user id's
def test_duplicate_user_id_conflict(client):
    client.post("/api/users", json=user_payload(uid=2))
    r = client.post("/api/users", json=user_payload(uid=2))
    assert r.status_code == 409 # duplicate id -> conflict
    assert "exists" in r.json()["detail"].lower()

# testing for bad student id's
@pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"])
def test_bad_student_id_422(client, bad_sid):
 r = client.post("/api/users", json=user_payload(uid=3, sid=bad_sid))
 assert r.status_code == 422 # pydantic validation e

# Testing for bad names
@pytest.mark.parametrize("bad_name", ["123", "A", "A123", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"])
def test_bad_student_id_422(client, bad_name):
 r = client.post("/api/users", json=user_payload(uid=3, sid=bad_name))
 assert r.status_code == 422 # pydantic validation e

