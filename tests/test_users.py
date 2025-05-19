from app.internal.database.models import User

payload = {
    "username": "alice",
    "first_name": "Alice",
    "last_name": "Smith",
    "email": "test@test.com",
}


def test_create_user(client):
    response = client.post("/users/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "id" in data


def test_get_user(client):
    post_resp = client.post("/users/", json=payload)
    assert post_resp.status_code == 201
    user_id = post_resp.json()["id"]

    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == user_id
    assert data["username"] == payload["username"]


def test_patch_user(client):
    post_resp = client.post("/users/", json=payload)
    assert post_resp.status_code == 201
    user_id = post_resp.json()["id"]

    update_data = {"first_name": "Alicja", "email": "nowy@email.com"}
    patch_resp = client.patch(f"/users/{user_id}", json=update_data)
    assert patch_resp.status_code == 200

    updated = patch_resp.json()
    assert updated["first_name"] == "Alicja"
    assert updated["email"] == "nowy@email.com"
    assert updated["id"] == user_id


def test_get_first_page_users(client, session):
    users_to_add = [
        User(
            username="alice",
            first_name="Alice",
            last_name="Smith",
            email="alice@test.com",
        ),
        User(username="bob", first_name="Bob", last_name="Brown", email="bob@test.com"),
        User(
            username="carol",
            first_name="Carol",
            last_name="Davis",
            email="carol@test.com",
        ),
    ]
    session.add_all(users_to_add)
    session.commit()

    response = client.get("/users/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3

    usernames = {user["username"] for user in data}
    assert usernames == {"alice", "bob", "carol"}
