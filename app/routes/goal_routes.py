from flask import Blueprint, request, Response, jsonify
from ..db import db
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_model, create_model

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json()
    goal_data, status_code = create_model(Goal, request_body)
    return jsonify({"goal": goal_data}), status_code


@bp.get("")
def get_all_goals():
    query = db.select(Goal)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Goal.title.ilike(f"%{title_param}%"))

    goals = db.session.scalars(query)

    return [goal.to_dict() for goal in goals]


@bp.get("/<id>")
def get_one_goal(id):
    goal = validate_model(Goal, id)
    return jsonify({"goal": goal.to_dict()}), 200


@bp.put("<id>")
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.delete("<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.post("/<id>/tasks")
def create_task_for_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    task_ids = request_body.get("task_ids", [])

    for task in goal.tasks:
        task.goal_id = None

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids
    }, 200


@bp.get("/<id>/tasks")
def get_tasks_for_goal(id):
    goal = validate_model(Goal, id)
    goal_dict = goal.to_dict()
    goal_dict["tasks"] = [task.to_dict() for task in goal.tasks]
    return goal_dict, 200