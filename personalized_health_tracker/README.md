# Personalized Health & Workout Tracker

A lightweight, Python-based CLI that helps you build a personalized health and workout log. Capture your profile, daily metrics, and workouts, then receive quick recommendations that keep you on track.

## Features
- **Profile onboarding** with primary goal tracking
- **Workout logging** with intensity, duration, and optional calories
- **Health metric capture** (e.g., weight, water intake)
- **Personalized nudges** for hydration, recovery, and goal milestones
- **JSON-backed storage** so data persists between runs without extra dependencies

## Getting Started
1. Ensure Python 3.10+ is available.
2. From the repository root, create a virtual environment (optional) and run commands via `python -m personalized_health_tracker.app.main`.

```bash
python -m personalized_health_tracker.app.main init-profile "Avery" 30 172 70 "5k training" 5 km
python -m personalized_health_tracker.app.main log-workout run 30 moderate --calories 280
python -m personalized_health_tracker.app.main log-metric water_intake 1.5 L
python -m personalized_health_tracker.app.main suggest
python -m personalized_health_tracker.app.main summary
```

State is stored at `personalized_health_tracker/data/state.json` by default. Override the path with `--state` if you want to separate environments (e.g., personal vs. demo).

## Project Layout
- `app/models.py`: Data models for profiles, goals, workouts, and metrics.
- `app/storage.py`: JSON persistence helpers.
- `app/recommender.py`: Lightweight recommendation rules.
- `app/main.py`: CLI entry point with subcommands.

## Ideas for Next Iterations
- Add calorie budgeting and macronutrient summaries
- Export data to CSV for dashboards
- Integrate heart-rate zones to personalize intensity guidance
