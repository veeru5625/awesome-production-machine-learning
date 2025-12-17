from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Goal:
    name: str
    target_value: float
    unit: str
    progress: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "target_value": self.target_value,
            "unit": self.unit,
            "progress": self.progress,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Goal":
        return cls(
            name=data.get("name", ""),
            target_value=float(data.get("target_value", 0.0)),
            unit=data.get("unit", ""),
            progress=float(data.get("progress", 0.0)),
        )


@dataclass
class WorkoutSession:
    workout_type: str
    duration_minutes: int
    intensity: str
    calories_burned: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict:
        return {
            "workout_type": self.workout_type,
            "duration_minutes": self.duration_minutes,
            "intensity": self.intensity,
            "calories_burned": self.calories_burned,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "WorkoutSession":
        timestamp = data.get("timestamp")
        parsed_timestamp = (
            datetime.fromisoformat(timestamp) if isinstance(timestamp, str) else datetime.utcnow()
        )
        return cls(
            workout_type=data.get("workout_type", "unknown"),
            duration_minutes=int(data.get("duration_minutes", 0)),
            intensity=data.get("intensity", "moderate"),
            calories_burned=(int(data["calories_burned"]) if data.get("calories_burned") else None),
            timestamp=parsed_timestamp,
        )


@dataclass
class HealthMetric:
    name: str
    value: float
    unit: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "HealthMetric":
        timestamp = data.get("timestamp")
        parsed_timestamp = (
            datetime.fromisoformat(timestamp) if isinstance(timestamp, str) else datetime.utcnow()
        )
        return cls(
            name=data.get("name", ""),
            value=float(data.get("value", 0.0)),
            unit=data.get("unit", ""),
            timestamp=parsed_timestamp,
        )


@dataclass
class UserProfile:
    name: str
    age: int
    height_cm: float
    weight_kg: float
    goals: List[Goal] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "age": self.age,
            "height_cm": self.height_cm,
            "weight_kg": self.weight_kg,
            "goals": [goal.to_dict() for goal in self.goals],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "UserProfile":
        return cls(
            name=data.get("name", ""),
            age=int(data.get("age", 0)),
            height_cm=float(data.get("height_cm", 0.0)),
            weight_kg=float(data.get("weight_kg", 0.0)),
            goals=[Goal.from_dict(goal) for goal in data.get("goals", [])],
        )
