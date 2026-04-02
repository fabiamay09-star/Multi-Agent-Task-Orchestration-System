from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import asyncio
import os

from backend.orchestrator import Orchestrator

app = FastAPI()

# Mount frontend
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

orchestrator = Orchestrator()

@app.get("/")
async def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await orchestrator.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # If we receive a task request
            await orchestrator.handle_task_request(data)
    except WebSocketDisconnect:
        orchestrator.disconnect(websocket)
