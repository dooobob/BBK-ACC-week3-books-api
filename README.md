# WEEK3 Books API

A simple application to create and retrieve books using FastAPI, SQLAlchemy, and SQLite.

## Requirements

```text
fastapi==0.141.1
uvicorn==0.52.4
sqlalchemy==2.0.55
pytest==9.1.1
httpx==0.28.1
```

## Install

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

## Endpoints

| Method | Path               | Description                |
| ------ | ------------------ | -------------------------- |
| GET    | `/`                | Check the API is running   |
| GET    | `/books`           | Retrieve all books         |
| GET    | `/books/{book_id}` | Retrieve a book by book ID |
| POST   | `/books`           | Create a book              |

API documentation: http://127.0.0.1:8000/docs

## API Testing

### Check the API

```http
GET /
```

#### Responses

| Status  | Data                                             | Description       |
| ------- | ------------------------------------------------ | ----------------- |
| **200** | `{"message":"Week 3 SQLAlchemy API is running"}` | Server is running |

### Create a book

```http
POST /books
DATA
{
  "title": "Clean Code",
  "author": "Robert Martin",
  "year": 2008
}
```

#### Responses

| Status  | Data                                                                 | Description                              |
| ------- | -------------------------------------------------------------------- | ---------------------------------------- |
| **201** | `{"id":1,"title":"Clean Code","author":"Robert Martin","year":2008}` | Book is created with a generated book_id |
| **422** | `{"detail":[...]}`                                                   | Request body fails validation            |

### Retrieve all books

```http
GET /books
```

#### Responses

| Status  | Data                                                                   | Description                            |
| ------- | ---------------------------------------------------------------------- | -------------------------------------- |
| **200** | `[]`                                                                   | Request success. But there is no book. |
| **200** | `[{"id":1,"title":"Clean Code","author":"Robert Martin","year":2008}]` | Retrieve all books                     |

### Retrieve the test book

```http
GET /books/1
```

#### Responses

| Status  | Data                                                                 | Description                      |
| ------- | -------------------------------------------------------------------- | -------------------------------- |
| **200** | `{"id":1,"title":"Clean Code","author":"Robert Martin","year":2008}` | Book matching the requested ID   |
| **404** | `{"detail":"Book not found"}`                                        | No book matches the requested ID |

## Validation and Error Handling

| Field    | Validation                                 |
| -------- | ------------------------------------------ |
| `title`  | Required string with at least 2 characters |
| `author` | Required string with at least 2 characters |
| `year`   | Required integer value, at least 1900      |

## Testing with TestClient

### Run each test files:

```bash
python -m pytest tests/test_api.py -v
python -m pytest tests/test_rules.py -v
```

### Run all test files

```bash
python -m pytest -q
```
