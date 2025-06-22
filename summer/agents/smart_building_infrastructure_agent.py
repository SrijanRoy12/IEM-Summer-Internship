import os
from dotenv import load_dotenv

class SmartBuildingInfrastructureAgent:
    def __init__(self, llm=None):
        self.llm = llm
        self.role = "Smart Building & Infrastructure"
        self.goal = "Simulate building sensors and automate energy-saving actions."
        self.backstory = "An AI agent that manages building operations and energy efficiency."
        self.name = "Smart Building & Infrastructure Agent"
        self.description = "Simulates building sensors and automates energy-saving actions."

    def act(self, context):
        return {
            "sensors": {"occupancy": 45, "lighting": "auto", "security": "secure"},
            "energy_action": "Lights dimmed and HVAC optimized for current occupancy."
        }

    def ask_llm(self, prompt):
        if self.llm:
            return self.llm(prompt)
        return "LLM not configured."

if __name__ == "__main__":
    load_dotenv()
    agent = SmartBuildingInfrastructureAgent()
    print(agent.act({}))
