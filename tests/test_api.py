from fastapi.testclient import TestClient

BOOK = {"title": "Clean Code", "author": "Robert Martin", "year": 2008}


def test_create_and_retrieve(client):
    created = client.post("/books", json=BOOK)
    assert created.status_code == 201
    body = created.json()
    assert body == {"id": body["id"], **BOOK}
    assert isinstance(body["id"], int)
    fetched = client.get(f"/books/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json() == body
    assert client.get("/books").json() == [body]


def test_invalid_input_does_not_add_row(client):
    response = client.post("/books", json={"title": "A", "author": "B", "year": 1800})
    assert response.status_code == 422
    assert all(
        any(error["loc"] == loc for error in response.json()["detail"])
        for loc in [["body", "title"], ["body", "author"], ["body", "year"]]
    )
    assert client.get("/books").json() == []


def test_missing_book(client):
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


def test_starts_empty(client):
    # This remains true even when other tests have created books.
    assert client.get("/books").json() == []


def test_data_survives_new_application(app_factory):
    with TestClient(app_factory()) as first:
        created = first.post("/books", json=BOOK)
        assert created.status_code == 201
        body = created.json()
    # A second app and new sessions use the same file within this test.
    with TestClient(app_factory()) as restarted:
        assert restarted.get(f"/books/{body['id']}").json() == body


def test_omiiting_required_data_does_not_add_row(client):
    request_data = BOOK.copy()
    del request_data["title"]
    response = client.post("/books", json=request_data)
    assert response.status_code == 422
    assert any(error["loc"] == ["body", "title"] for error in response.json()["detail"])
    assert client.get("/books").json() == []


def test_atomicity_after_invalidation_rejection(client):
    assert client.post("/books", json=BOOK).status_code == 201
    invalidation = client.post(
        "/books", json={"title": "A", "author": "B", "year": 1800}
    )
    assert invalidation.status_code == 422
    assert len(client.get("/books").json()) == 1
    new_book = {"title": "Human Acts", "author": "Han Kang", "year": 2014}
    created = client.post("/books", json=new_book)
    assert created.status_code == 201
    assert len(client.get("/books").json()) == 2
