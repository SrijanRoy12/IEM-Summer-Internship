import os
from dotenv import load_dotenv

class EmergencyAgent:
    def __init__(self, llm=None):
        self.llm = llm
        self.role = "Emergency Detection & Response"
        self.goal = "Detect emergencies and dispatch response units quickly."
        self.backstory = "An AI agent that listens to city sensors and coordinates emergency response."
        self.name = "Emergency Detection & Response Agent"
        self.description = "Detects emergencies and dispatches response units."

    def listen_to_sensors(self):
        # Simulate input from city sensors (fire, accident, etc.)
        return {"event": "fire", "location": "Hospital", "severity": "high"}

    def prioritize_and_dispatch(self, event):
        # Prioritize and dispatch emergency units
        return f"Dispatched fire unit to {event['location']} (Severity: {event['severity']})"

    def simulate_decision_path(self, scenario):
        # Placeholder for GPT-based simulation
        return f"If {scenario}, then dispatch additional units and alert TrafficAgent."

    def alert_traffic_agent(self):
        # Simulate alerting TrafficAgent
        return "Alert sent to TrafficAgent to clear roads."

    def run_training_simulation(self):
        # Simulate a training scenario
        return "Training simulation: fire in hospital, traffic rerouted, emergency response successful."

    def act(self, context):
        return {
            "emergency_event": "fire at Hospital",
            "dispatch_status": "Fire unit dispatched"
        }

    def ask_llm(self, prompt):
        if self.llm:
            return self.llm(prompt)
        return "LLM not configured."

if __name__ == "__main__":
    load_dotenv()
    agent = EmergencyAgent()
    event = agent.listen_to_sensors()
    print(event)
    print(agent.prioritize_and_dispatch(event))
    print(agent.simulate_decision_path("fire in hospital during traffic congestion"))
    print(agent.alert_traffic_agent())
    print(agent.run_training_simulation())
