from __future__ import annotations

from statistics import mean
from typing import List

from .models import Goal, HealthMetric, WorkoutSession


def hydration_prompt(metrics: List[HealthMetric]) -> str:
    water_entries = [m for m in metrics if m.name.lower() == "water_intake"]
    if not water_entries:
        return "Log your water intake to receive personalized hydration nudges."
    avg = mean([entry.value for entry in water_entries[-5:]])
    if avg < 2:
        return "Hydrate more: target at least 2L of water per day based on your recent logs."
    return "Great hydration! Keep maintaining 2L+ of water daily."


def workout_recommendation(workouts: List[WorkoutSession]) -> str:
    if not workouts:
        return "Add a 20-minute brisk walk to kickstart your activity streak today."
    last_session = workouts[-1]
    if last_session.intensity.lower() in {"high", "vigorous"}:
        return "Schedule a lighter recovery session (yoga or mobility) after yesterday's intense workout."
    return "Maintain momentum with a moderate 30-minute session; consider intervals to raise intensity."


def goal_progress_message(goals: List[Goal]) -> str:
    if not goals:
        return "Set a concrete goal (e.g., 5k in 6 weeks) to unlock tailored coaching."
    active = goals[0]
    progress_pct = min(100, (active.progress / active.target_value) * 100 if active.target_value else 0)
    return f"'{active.name}' is {progress_pct:.1f}% complete. Celebrate milestones every 10%!"


def build_recommendations(goals: List[Goal], workouts: List[WorkoutSession], metrics: List[HealthMetric]) -> List[str]:
    return [
        goal_progress_message(goals),
        workout_recommendation(workouts),
        hydration_prompt(metrics),
    ]
