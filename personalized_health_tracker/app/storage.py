from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from .models import HealthMetric, UserProfile, WorkoutSession

DEFAULT_STATE_PATH = Path(__file__).resolve().parents[1] / "data" / "state.json"


def _ensure_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps({"profile": {}, "workouts": [], "metrics": []}, indent=2))


def load_state(path: Path = DEFAULT_STATE_PATH) -> Dict:
    _ensure_file(path)
    with path.open() as f:
        data = json.load(f)
    return data


def save_state(profile: UserProfile, workouts: List[WorkoutSession], metrics: List[HealthMetric], path: Path = DEFAULT_STATE_PATH) -> None:
    payload = {
        "profile": profile.to_dict() if profile else {},
        "workouts": [workout.to_dict() for workout in workouts],
        "metrics": [metric.to_dict() for metric in metrics],
    }
    _ensure_file(path)
    path.write_text(json.dumps(payload, indent=2))


def load_objects(path: Path = DEFAULT_STATE_PATH):
    data = load_state(path)
    profile = UserProfile.from_dict(data.get("profile", {})) if data.get("profile") else None
    workouts = [WorkoutSession.from_dict(entry) for entry in data.get("workouts", [])]
    metrics = [HealthMetric.from_dict(entry) for entry in data.get("metrics", [])]
    return profile, workouts, metrics
