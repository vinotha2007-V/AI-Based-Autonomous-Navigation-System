
import json
from datetime import datetime
from pathlib import Path


def save_metrics(path, start, goal, route, status, elapsed_seconds):
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    metrics = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "algorithm": "A*",
        "start": list(start),
        "goal": list(goal),
        "status": status,
        "path_cells": len(route) if route else 0,
        "steps": max(0, len(route) - 1) if route else 0,
        "path_length": max(0, len(route) - 1) if route else 0,
        "collision_count": 0,
        "elapsed_seconds": round(elapsed_seconds, 4),
        "movement_model": "4-direction grid movement"
    }

    output_file = output_dir / "metrics.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4)

    print(f"Metrics saved to: {output_file}")
    return metrics
