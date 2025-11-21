### CSCI262 Assignment 3 Email system event modeler and intrusion detection system ###

Group Members:

Vernon Goh Shu Wei (UOW ID: 9071398)
Kaung Khant Kyaw (UOW ID: 8750154)
Chong Daryl (UOW ID: 9070394)
Wong Yiyang (UOW ID: 8336520)
Timothy Toh (UOW ID: 8931902)


Files Included:

    IDS.py
    activity_engine.py
    alert_engine.py
    alert.json (will be generated)
    analysis_engine.py
    baseline_analysis.json (will be generated)
    daily_logs_initial.json (will be generated)
    daily_logs_new.json (will be generated)
    Events.txt
    helper.py
    readme.txt
    Stats.txt
    Stats2.txt


To run:
	python IDS.py Events.txt Stats.txt <Days>

	#Example:
	python IDS.py Events.txt Stats.txt 5
	Press <Enter> to load the full logs
	
	#After the Analysis there will be 2 choices: stat or quit.
	#Example for stat:
	Type stat
	Press <Enter>
	"Enter days": 6
	Press <Enter> to load the full logs

	#Example for quit:
	Type quit
	Program ends



