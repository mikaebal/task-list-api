from app.db import db
from app.models.goal import Goal
import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_no_saved_goals(client):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_one_saved_goal(client, one_goal):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    ]


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goal(client, one_goal):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    }


# @pytest.mark.skip(reason="test to be completed by student")
def test_get_goal_not_found(client):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "details" in response_body
    assert response_body == {
        "details": "Goal 1 not found"
    }



# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal(client):
    # Act
    response = client.post("/goals", json={
        "title": "My New Goal"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "My New Goal"
        }
    }


# @pytest.mark.skip(reason="test to be completed by student")
def test_update_goal(client, one_goal):
    # raise Exception("Complete test")

    # Act
    response = client.put("/goals/1", json={
        "title": "Updated Goal Title"
    })

    # Assert
    assert response.status_code == 204

    query = db.select(Goal).where(Goal.id == 1)
    goal = db.session.scalar(query)

    assert goal.title == "Updated Goal Title"


# @pytest.mark.skip(reason="test to be completed by student")
def test_update_goal_not_found(client):
    #raise Exception("Complete test")

    # Act
    response = client.put("/goals/1", json={
        "title": "Updated Task Title"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "details" in response_body
    assert response_body == {
        "details": "Goal 1 not found"
    }


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_goal(client, one_goal):
    # Act
    response = client.delete("/goals/1")

    # Assert
    assert response.status_code == 204

    # Check that the goal was deleted
    response = client.get("/goals/1")
    assert response.status_code == 404

    response_body = response.get_json()
    assert "details" in response_body
    assert response_body == {
        "details": "Goal 1 not found"
    }


# @pytest.mark.skip(reason="test to be completed by student")
def test_delete_goal_not_found(client):
    # raise Exception("Complete test")

    # Act
    response = client.delete("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "details" in response_body
    assert response_body == {
        "details": "Goal 1 not found"
    }

    assert db.session.scalars(db.select(Goal)).all() == []


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal_missing_title(client):
    # Act
    response = client.post("/goals", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }
