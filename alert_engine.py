from analysis_engine import analyse_logs
import json

def alert_engine(logs, eventsList, baseline, anomoly_threshold):
    """Check new logs against baseline and trigger alerts if anomalies are detected."""
    for log in logs:
        total_anomaly_counter = 0
        for event, details in eventsList.items():
            baseline_mean = baseline[event]['mean']
            baseline_sd = baseline[event]['standard_deviation']
            log_value = log[event]

            if baseline_sd != 0:
                num_standard_deviations = (log_value - baseline_mean) / baseline_sd
                weighted_deviation = num_standard_deviations * details['weight']
                total_anomaly_counter += weighted_deviation
        
        # Check total anomaly counter against threshold
        if total_anomaly_counter > anomoly_threshold:
            log["status"] = "❌" * 10
        else:
            log["status"] = "✅" * 10
            
        log["anomaly_score"] = f"{round(total_anomaly_counter, 2)} / {anomoly_threshold}"
    
    print("\nAlerts generated for logs:")
    print(json.dumps(logs, indent=4, ensure_ascii=False))
    with open('alerts.json', 'w') as f:
        f.write(json.dumps(logs, indent=4))