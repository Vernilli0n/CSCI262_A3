import numpy as np
import json

# analyse logs to show total, mean and standard deviation which would be then outputted to a file
def analyse_logs(logs, events, type="baseline"):
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
            "standard_deviation": round(np.std(standard_deviation[event]), 2)  
        }

    with open(f'{type}_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=4)
        print(f"Analysis saved to {type}_analysis.json")
    return analysis