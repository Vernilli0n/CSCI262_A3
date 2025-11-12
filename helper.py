
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
                    'weight': float(parts[4])
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