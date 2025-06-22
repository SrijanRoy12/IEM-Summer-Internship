import os
os.environ["LITELLM_PROVIDER"] = "google"
from agents.traffic_agent import TrafficAgent
from agents.emergency_agent import EmergencyAgent
from agents.smart_energy_grid_agent import SmartEnergyGridAgent
from agents.healthcare_infrastructure_agent import HealthcareInfrastructureAgent
from agents.environmental_pollution_agent import EnvironmentalPollutionAgent
from agents.green_energy_sustainability_agent import GreenEnergySustainabilityAgent
from agents.smart_building_infrastructure_agent import SmartBuildingInfrastructureAgent
from agents.public_safety_crime_prevention_agent import PublicSafetyCrimePreventionAgent
from agents.urban_planning_development_agent import UrbanPlanningDevelopmentAgent
from utils.llm_utils import gemini_llm

class SmartCityOrchestrator:
    def __init__(self, llm_provider=gemini_llm):
        self.llm_provider = llm_provider
        self.traffic = TrafficAgent(llm=self.llm_provider)
        self.emergency = EmergencyAgent(llm=self.llm_provider)
        self.energy = SmartEnergyGridAgent(llm=self.llm_provider)
        self.healthcare = HealthcareInfrastructureAgent(llm=self.llm_provider)
        self.environment = EnvironmentalPollutionAgent(llm=self.llm_provider)
        self.green = GreenEnergySustainabilityAgent(llm=self.llm_provider)
        self.building = SmartBuildingInfrastructureAgent(llm=self.llm_provider)
        self.safety = PublicSafetyCrimePreventionAgent(llm=self.llm_provider)
        self.urban = UrbanPlanningDevelopmentAgent(llm=self.llm_provider)

    def run_scenario(self, scenario, user_input=None):
        logs = [f"Scenario: {scenario}"]
        context = {"scenario": scenario, "user_input": user_input}
        logs.append(str(self.traffic.act(context)))
        logs.append(str(self.emergency.act(context)))
        logs.append(str(self.energy.act(context)))
        logs.append(str(self.healthcare.act(context)))
        logs.append(str(self.environment.act(context)))
        logs.append(str(self.green.act(context)))
        logs.append(str(self.building.act(context)))
        logs.append(str(self.safety.act(context)))
        logs.append(str(self.urban.act(context)))
        return logs
