import sys
import time
from helper import *
from activity_engine import generate_events
from analysis_engine import analyse_logs
import json

def main():
    #accept command line arguments
    days = sys.argv[3] if len(sys.argv) > 3 else 5
    eventsFile = sys.argv[1] if len(sys.argv) > 1 else "Events.txt"
    statsFile = sys.argv[2] if len(sys.argv) > 2 else "Stats.txt"
    
    #load data from files
    eventsList = load_events(eventsFile)
    statsList = load_stats(statsFile)

    print("Loading event and stats data...")
    time.sleep(2) #lmao
    print(json.dumps(eventsList, indent=4))
    print(json.dumps(statsList, indent=4))

    # Generate events accoerding to loaded data
    print(f"Generating logs for {days} days...")
    input ("Press Enter to continue...")
    logs = generate_events(eventsList, statsList, int(days), "initial")
    print(json.dumps(logs, indent=4))

    print("\nAnalyzing generated logs to set baselines...")
    input ("Press Enter to continue...")
    # Analyse generated logs to set baselines
    baseline = analyse_logs(logs, eventsList)
    print(json.dumps(baseline, indent=4))

    print("\n\nProcess completed. Generated logs saved to 'daily_logs_initial.json' and analysis saved to 'baseline_analysis.json'.")
    statsFile = input ("Enter the next stats file to load:\t")
    print(f"Loading stats from {statsFile}...")
    time.sleep(2) #lmao
    newStatsList = load_stats(statsFile)
    print("Loaded new stats:")
    print(json.dumps(newStatsList, indent=4))

    # Generate new logs based on new stats
    days = input("Enter number of days to generate logs for:\t")
    print(f"Generating logs for {days} days with new stats...")
    input ("Press Enter to continue...")
    newLogs = generate_events(eventsList, newStatsList, int(days), "new")
    print(json.dumps(newLogs, indent=4))



main()