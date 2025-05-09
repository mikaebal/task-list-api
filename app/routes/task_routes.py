from flask import Blueprint, request, Response, jsonify
from ..db import db
from app.models.task import Task
from .route_utilities import validate_model, create_model
from datetime import datetime
import requests, os


bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@bp.post("")
def create_task():
    request_body = request.get_json()
    task_data, status_code = create_model(Task, request_body)
    return jsonify({"task": task_data}), status_code


@bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    sort_param = request.args.get("sort")
    if sort_param == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.title.asc())

    tasks = db.session.scalars(query)

    return [task.to_dict() for task in tasks]


@bp.get("/<id>")
def get_one_task(id):
    task = validate_model(Task, id)
    return jsonify({"task": task.to_dict()}), 200


@bp.put("/<id>")
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task, id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.patch("/<id>/mark_complete")
def mark_complete(id):
    task = validate_model(Task, id)
    if task.completed_at is None:
        task.completed_at = datetime.now()
        db.session.commit()

        slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
        slack_channel = os.environ.get("SLACK_CHANNEL", "task-notifications")

        headers = {
                "Authorization": f"Bearer {slack_bot_token}"
            }

        payload = {
                "channel": slack_channel,
                "text": f"Someone just completed the task {task.title}"
            }

        requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=payload)

    return Response(status=204, mimetype="application/json")


@bp.patch("/<id>/mark_incomplete")
def mark_incomplete(id):
    task = validate_model(Task, id)
    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")
