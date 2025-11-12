import sys
from helper import *
from activity_engine import generate_events
import json

def main():
    days = sys.argv[3] if len(sys.argv) > 3 else 5
    eventsFile = sys.argv[1] if len(sys.argv) > 1 else "Events.txt"
    statsFile = sys.argv[2] if len(sys.argv) > 2 else "Stats.txt"
    eventsList = load_events(eventsFile)
    statsList = load_stats(statsFile)

    #print(json.dumps(eventsList, indent=4))
    #print(json.dumps(statsList, indent=4))
    
    logs = generate_events(eventsList, statsList, int(days))

    print(json.dumps(logs, indent=4))

main()