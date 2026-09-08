# Focus List

Focus List is a simple full-stack to-do list application for creating, completing, and deleting daily tasks. It has a clean browser interface and a REST API, with both services storing tasks in the same SQLite database.

## Features

- Add tasks from the web interface
- Mark tasks as complete or incomplete
- Delete individual tasks or clear all completed tasks
- Persist tasks with SQLAlchemy and SQLite
- Manage tasks programmatically through FastAPI REST endpoints
- Browse interactive FastAPI documentation at `/docs`

## Technology used

| Layer | Technology |
| --- | --- |
| Frontend | HTML, CSS, JavaScript |
| Web application | Flask |
| Database ORM | SQLAlchemy |
| Database | SQLite |
| REST API | FastAPI |

## Project structure

```text
TO-DO-List/
├── app.py          # Flask app and web UI endpoints
├── api.py          # FastAPI REST API
├── database.py     # SQLAlchemy database configuration
├── models.py       # To-do database model
├── templates/      # HTML templates
├── static/         # CSS and JavaScript assets
└── requirements.txt
```

## Run it

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` for the web app.

To run the FastAPI service (with interactive docs at `/docs`):

```powershell
uvicorn api:app --reload --port 8000
```

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/todos` | Get all tasks |
| `POST` | `/api/todos` | Create a task |
| `PATCH` | `/api/todos/{todo_id}` | Update a task's title or completion status |
| `DELETE` | `/api/todos/{todo_id}` | Delete a task |

Example request body for creating a task:

```json
{
  "title": "Finish my project"
}
```
