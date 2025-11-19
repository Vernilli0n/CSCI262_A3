import sys
import time
import os
from helper import *
from activity_engine import generate_events
from analysis_engine import analyse_logs
from alert_engine import alert_engine
import json

# selects a file form terminal, default or prompts user
def _choose_file_from_args(arg_index: int, default_name: str, prompt: str) -> str:
    if len(sys.argv) > arg_index:
        candidate = sys.argv[arg_index]
        if os.path.isfile(candidate):
            return candidate
        print(f"'{candidate}' does not exist.")
    if os.path.isfile(default_name):
        print(f"Using default: {default_name}")
        return default_name
    return ask_for_existing_file(prompt)

def main():
    # decides files/days from argv or prompt/ defaults
    eventsFile = _choose_file_from_args(1, "Events.txt", "Enter events file to load: ")
    statsFile = _choose_file_from_args(2, "Stats.txt", "Enter stats file to load: ")

    # determines days by preferring argv value if valid integer, otherwise prompt
    days = None
    if len(sys.argv) > 3:
        try:
            days = int(sys.argv[3])
            if days < 1:
                raise ValueError
        except ValueError:
            print(f"Invalid days value '{sys.argv[3]}'. Please enter a positive integer.")
            days = ask_for_positive_int("Enter number of days to generate logs for: ")
    else:
        days = ask_for_positive_int("Enter number of days to generate logs for: ")

    # loads the data from files
    eventsList = load_events(eventsFile)
    statsList = load_stats(statsFile)
    anomaly_threshold = calculate_anomaly_threshold(eventsList)

    print("Loading event and stats data...")
    print(json.dumps(eventsList, indent=4))
    print(json.dumps(statsList, indent=4))

    # generates events according to loaded data
    print(f"Generating logs for {days} days...")
    input("Press Enter to continue...")
    logs = generate_events(eventsList, statsList, days, "initial")
    print(json.dumps(logs, indent=4))

    print("\nAnalyzing generated logs to set baselines...")
    input("Press Enter to continue...")
    baseline = analyse_logs(logs, eventsList)
    print(json.dumps(baseline, indent=4))

    print("\n\nProcess completed, the generated logs are saved to 'daily_logs_initial.json' and analysis saved to 'baseline_analysis.json'.")
    
    # loop implementated to allow user to load multiple stats files and specify days repeatedly
    analysis_round = 1
    while True:
        print(f"\n Analysis Round {analysis_round}")
        user_choice = input("\nOptions:\n  [stat] Load another stats file and analyze\n  [quit] Quit\n\nEnter your choice: ").strip().lower()
        if user_choice == 'quit':
            print("End of analysis, exiting the program.")
            break
        elif user_choice != 'stat':
            print("Invalid choice. Please enter 'stat' or 'quit'.")
            continue
        
        # next round of stats input that allows user to press Enter to use Stats2.txt or enter a different existing file
        next_stats = input("Enter the next stats file to load (press Enter to use 'Stats2.txt'):\t").strip()
        if not next_stats:
            next_stats = "Stats2.txt" if os.path.isfile("Stats2.txt") else ask_for_existing_file("Enter the next stats file to load: ")
        elif not os.path.isfile(next_stats):
            print(f"'{next_stats}' does not exist.")
            next_stats = ask_for_existing_file("Enter the next stats file to load: ")
        print(f"Loading stats from {next_stats}...")
        newStatsList = load_stats(next_stats)
        print("Loaded new stats:")
        print(json.dumps(newStatsList, indent=4))

        # generates new logs based on new stats
        days = ask_for_positive_int("Enter number of days to generate logs for: ")
        print(f"Generating logs for {days} days with new stats...")
        input("Press Enter to continue...")
        newLogs = generate_events(eventsList, newStatsList, days, "new")
        print(json.dumps(newLogs, indent=4))

        # checks for anomalies using alert engine
        print("\nAnalyzing new logs for anomalies...")
        input("Press Enter to continue...")
        alert_engine(newLogs, eventsList, baseline, anomaly_threshold)
        print ("\nAlerts saved to 'alerts.json'.")
        print(f"\nRound {analysis_round} completed.")
        
        analysis_round += 1

if __name__ == "__main__":
    main()