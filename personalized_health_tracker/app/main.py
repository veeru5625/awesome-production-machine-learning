from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import List

from .models import Goal, HealthMetric, UserProfile, WorkoutSession
from .recommender import build_recommendations
from .storage import DEFAULT_STATE_PATH, load_objects, save_state


def init_profile(args: argparse.Namespace) -> None:
    goal = Goal(name=args.goal_name, target_value=args.goal_target, unit=args.goal_unit, progress=0)
    profile = UserProfile(
        name=args.name,
        age=args.age,
        height_cm=args.height_cm,
        weight_kg=args.weight_kg,
        goals=[goal],
    )
    save_state(profile, workouts=[], metrics=[], path=args.state)
    print(f"Initialized profile for {profile.name} with goal '{goal.name}'.")


def log_workout(args: argparse.Namespace) -> None:
    profile, workouts, metrics = load_objects(args.state)
    if not profile:
        raise SystemExit("Create a profile first with 'init-profile'.")
    session = WorkoutSession(
        workout_type=args.workout_type,
        duration_minutes=args.duration,
        intensity=args.intensity,
        calories_burned=args.calories,
        timestamp=datetime.utcnow(),
    )
    workouts.append(session)
    save_state(profile, workouts, metrics, path=args.state)
    print(f"Logged {session.duration_minutes} minute {session.workout_type} session at {session.intensity} intensity.")


def log_metric(args: argparse.Namespace) -> None:
    profile, workouts, metrics = load_objects(args.state)
    if not profile:
        raise SystemExit("Create a profile first with 'init-profile'.")
    metric = HealthMetric(name=args.name, value=args.value, unit=args.unit)
    metrics.append(metric)
    save_state(profile, workouts, metrics, path=args.state)
    print(f"Recorded metric {metric.name}: {metric.value}{metric.unit}.")


def show_summary(args: argparse.Namespace) -> None:
    profile, workouts, metrics = load_objects(args.state)
    if not profile:
        raise SystemExit("Create a profile first with 'init-profile'.")

    print("Profile")
    print(f"- Name: {profile.name}")
    print(f"- Age: {profile.age}")
    print(f"- Height: {profile.height_cm} cm")
    print(f"- Weight: {profile.weight_kg} kg")
    print("\nGoals")
    for goal in profile.goals:
        progress_pct = (goal.progress / goal.target_value) * 100 if goal.target_value else 0
        print(f"- {goal.name}: {goal.progress}{goal.unit} of {goal.target_value}{goal.unit} ({progress_pct:.1f}%)")

    print("\nRecent workouts (last 5)")
    for session in workouts[-5:]:
        print(
            f"- {session.workout_type} for {session.duration_minutes} min @ {session.intensity} intensity"
            + (f" ({session.calories_burned} kcal)" if session.calories_burned else "")
        )

    print("\nRecent metrics (last 5)")
    for metric in metrics[-5:]:
        print(f"- {metric.name}: {metric.value}{metric.unit}")


def suggest(args: argparse.Namespace) -> None:
    profile, workouts, metrics = load_objects(args.state)
    if not profile:
        raise SystemExit("Create a profile first with 'init-profile'.")
    recommendations = build_recommendations(profile.goals, workouts, metrics)
    print("Personalized recommendations:")
    for rec in recommendations:
        print(f"- {rec}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Personalized Health & Workout Tracker")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE_PATH, help="Path to JSON state file")
    subparsers = parser.add_subparsers(dest="command", required=True)

    profile_parser = subparsers.add_parser("init-profile", help="Create a user profile")
    profile_parser.add_argument("name", type=str, help="User name")
    profile_parser.add_argument("age", type=int, help="User age")
    profile_parser.add_argument("height_cm", type=float, help="Height in centimeters")
    profile_parser.add_argument("weight_kg", type=float, help="Weight in kilograms")
    profile_parser.add_argument("goal_name", type=str, help="Primary goal description")
    profile_parser.add_argument("goal_target", type=float, help="Goal target value")
    profile_parser.add_argument("goal_unit", type=str, help="Unit for the goal (e.g., km, kg)")
    profile_parser.set_defaults(func=init_profile)

    workout_parser = subparsers.add_parser("log-workout", help="Add a workout session")
    workout_parser.add_argument("workout_type", type=str, help="Type of workout")
    workout_parser.add_argument("duration", type=int, help="Duration in minutes")
    workout_parser.add_argument("intensity", type=str, choices=["low", "moderate", "high", "vigorous"], help="Intensity level")
    workout_parser.add_argument("--calories", type=int, default=None, help="Calories burned (optional)")
    workout_parser.set_defaults(func=log_workout)

    metric_parser = subparsers.add_parser("log-metric", help="Record a health metric")
    metric_parser.add_argument("name", type=str, help="Metric name (e.g., weight, water_intake)")
    metric_parser.add_argument("value", type=float, help="Metric value")
    metric_parser.add_argument("unit", type=str, help="Metric unit")
    metric_parser.set_defaults(func=log_metric)

    summary_parser = subparsers.add_parser("summary", help="Show profile and recent activity")
    summary_parser.set_defaults(func=show_summary)

    suggest_parser = subparsers.add_parser("suggest", help="Get personalized nudges")
    suggest_parser.set_defaults(func=suggest)

    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
