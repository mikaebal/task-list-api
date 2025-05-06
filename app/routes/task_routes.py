from flask import Blueprint, request, Response, jsonify
from ..db import db
from app.models.task import Task
from .route_utilities import validate_model

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# POST /tasks 
@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400
    
    task = Task.from_dict(request_body)
    db.session.add(task)
    db.session.commit()

    return jsonify({"task": task.to_dict()}), 201


# GET /tasks
@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    query = query.order_by(Task.title.asc())
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return tasks_response


# GET /tasks/1
@tasks_bp.get("/<id>")
def get_one_task(id):
    task = validate_model(Task, id)
    return jsonify({"task": task.to_dict()}), 200


# PUT /tasks/1 
@tasks_bp.put("/<id>")
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")


# DELETE /tasks/1
@tasks_bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task, id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
