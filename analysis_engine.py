import numpy as np
import json


def analyse_logs(logs, events):
    analysis = {}
    total_days = len(logs)
    count = {event: 0 for event in events.keys()}
    standard_deviation = {event: [] for event in events.keys()}
    print(json.dumps(count, indent=4))
    for log in logs:
        for event in events.keys():
            count[event] += log[event]
            standard_deviation[event].append(log[event])
        
    for event in events.keys():
        analysis[event] = {
            "total": count[event],
            "mean": round(count[event] / total_days, 2),
            "standard_deviation": round(np.std(standard_deviation[event]), 2)  # Placeholder for standard deviation calculation
        }

    with open('analysis.json', 'w') as f:
        json.dump(analysis, f, indent=4)
        print("Analysis saved to analysis.json")
    return analysis