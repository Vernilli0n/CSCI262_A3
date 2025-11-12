
class events:
    def __init__(self, event_name, event_type, minimum, maximum, weight):
        self.event_name = event_name
        self.event_type = event_type
        self.minimum = minimum
        self.maximum = maximum
        self.weight = weight

    def display_event(self):
        print(f"Event Name: {self.event_name}, Type: {self.event_type}, Min: {self.minimum}, Max: {self.maximum}, Weight: {self.weight}")