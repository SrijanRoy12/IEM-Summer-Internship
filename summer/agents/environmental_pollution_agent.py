import os
from dotenv import load_dotenv

class EnvironmentalPollutionAgent:
    def __init__(self, llm=None):
        self.llm = llm
        self.role = "Environmental & Pollution Control"
        self.goal = "Monitor and predict pollution, suggest controls."
        self.backstory = "An AI agent that monitors air, noise, and water quality and predicts pollution spikes."
        self.name = "Environmental & Pollution Control Agent"
        self.description = "Monitors and predicts pollution, suggests controls."

    def act(self, context):
        return {
            "air_quality": "moderate",
            "noise_level": "high",
            "water_quality": "good",
            "pollution_alert": "Air pollution spike expected near Industrial Zone in 1 hour."
        }

    def ask_llm(self, prompt):
        if self.llm:
            return self.llm(prompt)
        return "LLM not configured."

if __name__ == "__main__":
    load_dotenv()
    agent = EnvironmentalPollutionAgent()
    print(agent.act({}))
