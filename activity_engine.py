import random

def generate_events(events, stats, days, multiplier=1 ):
    logs = []
    
    for day in range(1, days +1):
        daily_log = {}
        
        for event, event_details in events.items():
            if event_details['type'] == 'C':
                value = round(random.gauss(stats[event]['mean'], stats[event]['sd']), 2)
            else:
                value = max(0, round(random.gauss(stats[event]['mean'], stats[event]['sd']))) 

            daily_log[event] = max(event_details['mini'], min(value * multiplier, event_details['maxi']))
        
        logs.append(daily_log)
    
    return logs