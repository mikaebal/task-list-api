from flask import Blueprint, request, Response, jsonify
from ..db import db
from app.models.goal import Goal
from .route_utilities import validate_model
# import requests, os

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# POST request to /goals
# invalid request is {} --> 400
@bp.post("")
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    
    goal = Goal.from_dict(request_body)
    db.session.add(goal)
    db.session.commit()

    return jsonify({"goal": goal.to_dict()}), 201


# GET request to /goals
# GET request to /goals 0 saved goals --> response 200 ok []
@bp.get("")
def get_all_goals():
    query = db.select(Goal)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Goal.title.ilike(f"%{title_param}%"))

    goals = db.session.scalars(query)

    return [goal.to_dict() for goal in goals]


# GET request to /goals/1
@bp.get("/<id>")
def get_one_goal(id):
    goal = validate_model(Goal, id)
    return jsonify({"goal": goal.to_dict()}), 200


# PUT request to /goals/1
@bp.put("<id>")
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")


# DELETE request to /goals/1
@bp.delete("<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
