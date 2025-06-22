import os
from dotenv import load_dotenv

class TrafficAgent:
    def __init__(self, llm=None):
        self.llm = llm
        self.role = "Traffic Control & Optimization"
        self.goal = "Optimize traffic flow and reduce congestion."
        self.backstory = "An AI agent responsible for monitoring and managing city traffic in real time."
        self.name = "Traffic Control & Optimization Agent"
        self.description = "Monitors traffic, predicts congestion, and adjusts signals."

    def act(self, context):
        return {
            "traffic_status": "moderate",
            "congestion_prediction": "Main St congestion in 15 min"
        }

    # Example method for LLM integration (OpenAI/Gemini)
    def ask_llm(self, prompt):
        if self.llm:
            return self.llm(prompt)
        return "LLM not configured."

if __name__ == "__main__":
    load_dotenv()
    agent = TrafficAgent()
    print(agent.act(None))
    print(agent.ask_llm("What's the traffic status on Main St?"))
