import json
import asyncio
from typing import List
from fastapi import WebSocket
from backend.agents import PlannerAgent, get_agent_by_type

class Orchestrator:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

    async def update_agent_status(self, agent_name: str, status: str, log: str):
        await self.broadcast({
            "type": "agent_update",
            "agent": agent_name,
            "status": status,
            "log": log
        })

    async def append_system_log(self, log: str):
        await self.broadcast({
            "type": "system_log",
            "log": log
        })

    async def handle_task_request(self, data_str: str):
        # We start a background task so the websocket loop isn't blocked
        data = json.loads(data_str)
        task_description = data.get("task", "")
        asyncio.create_task(self.run_orchestration(task_description))

    async def run_orchestration(self, main_task: str):
        await self.append_system_log(f"Starting orchestration for: '{main_task}'")
        
        # Step 1: Planner
        planner = PlannerAgent()
        await self.append_system_log("Planner is breaking down the task.")
        plan = await planner.execute(main_task, {}, self.update_agent_status)
        
        await self.broadcast({
            "type": "plan_created",
            "plan": plan
        })
        
        context = {"main_task": main_task}
        
        # Step 2: Execute Plan
        for step in plan:
            agent_type = step["agent_type"]
            description = step["description"]
            
            agent = get_agent_by_type(agent_type)
            await self.append_system_log(f"Assigning step {step['step']} to {agent.name}: {description}")
            
            result = await agent.execute(description, context, self.update_agent_status)
            context[agent_type] = result
            
            # Additional sleep for aesthetic UI pacing
            await asyncio.sleep(1)
        
        await self.append_system_log("Orchestration complete.")
        await self.broadcast({
            "type": "orchestration_complete",
            "result": "All steps finished successfully."
        })
