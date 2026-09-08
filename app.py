from flask import Flask, jsonify, render_template, request
from database import Base, SessionLocal, engine
from models import Todo

app = Flask(__name__)
Base.metadata.create_all(bind=engine)


def serialize(todo):
    return {"id": todo.id, "title": todo.title, "completed": todo.completed, "created_at": todo.created_at.isoformat()}


@app.get("/")
def index():
    return render_template("index.html")


@app.route("/todos", methods=["GET", "POST"])
def todos():
    db = SessionLocal()
    try:
        if request.method == "GET":
            return jsonify([serialize(item) for item in db.query(Todo).order_by(Todo.completed, Todo.created_at.desc()).all()])
        title = str((request.get_json(silent=True) or {}).get("title", "")).strip()
        if not title:
            return jsonify({"error": "A task title is required."}), 400
        item = Todo(title=title)
        db.add(item); db.commit(); db.refresh(item)
        return jsonify(serialize(item)), 201
    finally:
        db.close()


@app.route("/todos/<int:todo_id>", methods=["PATCH", "DELETE"])
def todo(todo_id):
    db = SessionLocal()
    try:
        item = db.get(Todo, todo_id)
        if not item:
            return jsonify({"error": "Task not found."}), 404
        if request.method == "DELETE":
            db.delete(item); db.commit()
            return "", 204
        data = request.get_json(silent=True) or {}
        if "title" in data:
            title = str(data["title"]).strip()
            if not title:
                return jsonify({"error": "A task title is required."}), 400
            item.title = title
        if "completed" in data:
            item.completed = bool(data["completed"])
        db.commit(); db.refresh(item)
        return jsonify(serialize(item))
    finally:
        db.close()


if __name__ == "__main__":
    app.run(debug=True)
