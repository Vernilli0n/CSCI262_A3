import random
import json

def generate_events(events, stats, days, type, multiplier=1 ):
    logs = []
    
    for day in range(1, days +1):
        daily_log = {"day": day}
        for event, event_details in events.items():
            if event_details['type'] == 'C':
                value = round(random.gauss(stats[event]['mean'], stats[event]['sd']), 2)
            else:
                value = max(0, round(random.gauss(stats[event]['mean'], stats[event]['sd']))) 

            daily_log[event] = max(event_details['min'], min(value * multiplier, event_details['maxi'] if event_details['maxi'] is not None else value))
        logs.append(daily_log)
    
    with open(f'daily_logs_{type}.json', 'w') as f:
        json.dump(logs, f, indent=4)
    return logs