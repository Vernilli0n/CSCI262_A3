import os
import logging
from typing import Dict, Any, Optional

def ask_for_existing_file(prompt_text: str = "Enter file path: ") -> str:
    while True:
        p = input(prompt_text).strip()
        if os.path.isfile(p):
            return p
        print(f"'{p}' does not exist. Please enter a valid file.")

def ask_for_positive_int(prompt: str = "Enter number of days to generate logs for: ",
                        min_value: int = 1, allow_zero: bool = False) -> int:
    while True:
        s = input(prompt).strip()
        try:
            v = int(s)
        except ValueError:
            print(f"'{s}' is not a valid integer. Please enter a number.")
            continue
        if (allow_zero and v < 0) or (not allow_zero and v < min_value):
            print(f"Please enter an integer {'>= 0' if allow_zero else f'>= {min_value}'}")
            continue
        return v

def _to_int(s: str, default: Optional[int] = None, abs_val: bool = False) -> Optional[int]:
    try:
        v = int(s) if s != "" else default
        return abs(v) if (v is not None and abs_val) else v
    except (ValueError, TypeError):
        return default

def _ensure_path(file_path: Optional[str], prompt: str) -> str:
    if not file_path or not os.path.isfile(file_path):
        logging.warning("File not found or not provided: %s", file_path)
        return ask_for_existing_file(prompt)
    return file_path

def load_events(file_path: str) -> Dict[str, Dict[str, Any]]:
    events: Dict[str, Dict[str, Any]] = {}
    path = _ensure_path(file_path, "Enter events file path: ")
    try:
        with open(path, encoding="utf-8") as f:
            for lineno, raw in enumerate(f, 1):
                line = raw.strip()
                if not line or line.startswith(('#', '//')):
                    continue
                parts = line.split(':')
                if len(parts) < 5:
                    logging.warning("Skipping malformed events line %d: %s", lineno, line)
                    continue
                key = parts[0]
                min_val = _to_int(parts[2], default=None)
                maxi = _to_int(parts[3], default=None)
                weight = _to_int(parts[4], default=1, abs_val=True) or 1
                events[key] = {
                    "type": parts[1] if len(parts) > 1 else "",
                    "min": min_val,
                    "maxi": maxi,
                    "weight": weight,
                }
    except Exception as e:
        logging.error("Failed to read events file %s: %s", path, e)
    return events

def load_stats(file_path: str) -> Dict[str, Dict[str, Any]]:
    stats: Dict[str, Dict[str, Any]] = {}
    path = _ensure_path(file_path, "Enter the next stats file to load: ")
    try:
        with open(path, encoding="utf-8") as f:
            for lineno, raw in enumerate(f, 1):
                line = raw.strip()
                if not line or line.startswith(('#', '//')):
                    continue
                parts = line.split(':')
                if len(parts) < 3:
                    logging.warning("Skipping malformed stats line %d: %s", lineno, line)
                    continue
                try:
                    mean = float(parts[1])
                except ValueError:
                    logging.warning("Invalid mean on line %d for %s, skipping", lineno, parts[0])
                    continue
                try:
                    sd = float(parts[2])
                except ValueError:
                    logging.warning("Invalid sd on line %d for %s, setting sd=None", lineno, parts[0])
                    sd = None
                stats[parts[0]] = {"mean": mean, "sd": sd}
    except Exception as e:
        logging.error("Failed to read stats file %s: %s", path, e)
    return stats

def calculate_anomaly_threshold(events: Dict[str, Dict[str, Any]]) -> float:
    if not isinstance(events, dict):
        logging.error("calculate_anomaly_threshold expects a dict, got %s", type(events).__name__)
        return 0.0
    total = 0.0
    for d in events.values():
        try:
            total += float(d.get("weight", 0))
        except Exception:
            continue
    return total * 2.0