import asyncio
import random

class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.status = "idle"

    async def execute(self, task: str, context: dict, callback):
        await callback(self.name, "working", "Initializing dependencies...")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        await callback(self.name, "working", f"Processing chunk: {task[:20]}...")
        await asyncio.sleep(random.uniform(1.0, 2.5))
        
        result = self.perform_work(task, context)
        
        await callback(self.name, "finished", "Task efficiently resolved.")
        return result

    def perform_work(self, task: str, context: dict):
        return f"Result from {self.name}"

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Planner", "Breaks down tasks into steps")
    
    def perform_work(self, task: str, context: dict):
        return [
            {"step": 1, "agent_type": "Researcher", "description": f"Gather context about '{task}'"},
            {"step": 2, "agent_type": "Coder", "description": f"Develop implementation for '{task}'"},
            {"step": 3, "agent_type": "Reviewer", "description": f"Review generated artifacts"}
        ]

class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__("Researcher", "Gathers information")

class CoderAgent(BaseAgent):
    def __init__(self):
        super().__init__("Coder", "Writes code / creates solutions")

class ReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Reviewer", "Reviews code and output")

def get_agent_by_type(agent_type: str):
    agents = {
        "Researcher": ResearcherAgent(),
        "Coder": CoderAgent(),
        "Reviewer": ReviewerAgent(),
        "Planner": PlannerAgent()
    }
    return agents.get(agent_type, ResearcherAgent())
