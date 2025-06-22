import os
from dotenv import load_dotenv

class UrbanPlanningDevelopmentAgent:
    def __init__(self, llm=None):
        self.llm = llm
        self.role = "Urban Planning & Development"
        self.goal = "Analyze city data and propose infrastructure changes."
        self.backstory = "An AI agent that plans city growth and simulates development impacts."
        self.name = "Urban Planning & Development Agent"
        self.description = "Analyzes city data and proposes infrastructure changes."

    def act(self, context):
        return {
            "city_data": {
                "population": 500000,
                "traffic_density": "high",
                "utility_usage": {"water": 12000, "electricity": 45000}
            },
            "proposal": "Proposed new hospital and road expansion in North District."
        }

    def ask_llm(self, prompt):
        if self.llm:
            return self.llm(prompt)
        return "LLM not configured."

if __name__ == "__main__":
    load_dotenv()
    agent = UrbanPlanningDevelopmentAgent()
    print(agent.act({}))
