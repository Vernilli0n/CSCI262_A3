
def load_events(file_path):
    """Load data from a given file path."""
    events_list = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 6:
                events_list[parts[0]] = {
                    'type': parts[1],
                    'min': int(parts[2]),
                    'maxi': int(parts[3]) if parts[3] else None,
                    'weight': abs(int(parts[4])) if parts[4] else print("No weight specified, defaulting to 1") or 1,
                }
    return events_list

def load_stats(file_path):
    """Load stats from a given file path."""
    stats_list = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 4:
                stats_list[parts[0]] = {
                    'mean': float(parts[1]),
                    'sd': float(parts[2])
                }
    return stats_list

def calculate_anomaly_threshold(events):
    """Calculate anomaly threshold based on events weights."""
    threshold = 0
    for event, details in events.items():
        threshold += details['weight']
    return threshold * 2