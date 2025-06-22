import os
from dotenv import load_dotenv

class PublicSafetyCrimePreventionAgent:
    def __init__(self, llm=None):
        self.llm = llm
        self.role = "Public Safety & Crime Prevention"
        self.goal = "Simulate camera feeds and route police units."
        self.backstory = "An AI agent that monitors public safety and coordinates police response."
        self.name = "Public Safety & Crime Prevention Agent"
        self.description = "Simulates camera feeds and routes police units."

    def act(self, context):
        return {
            "camera_event": {"camera_id": 101, "event": "suspicious motion detected", "location": "Central Park"},
            "police_action": "Police unit dispatched to Central Park."
        }

    def ask_llm(self, prompt):
        if self.llm:
            return self.llm(prompt)
        return "LLM not configured."

if __name__ == "__main__":
    load_dotenv()
    agent = PublicSafetyCrimePreventionAgent()
    event = agent.simulate_camera_feed()
    print(event)
    print(agent.interpret_threats(event))
    print(agent.track_and_route_police(event["location"]))
    print(agent.collaborate_with_emergency())
    print(agent.generate_crime_heatmap())
