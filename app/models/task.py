from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from typing import Optional
from datetime import datetime
from flask import abort, make_response

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def to_dict(self):
        return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.completed_at is not None   #bool(self.completed_at)
        }

    @classmethod
    def from_dict(cls, task_data):
        # clean option for post create task
        # if "title" not in task_data or "description" not in task_data:
        #     abort(make_response({"details": "Invalid data"}, 400))
    
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at")
        )
