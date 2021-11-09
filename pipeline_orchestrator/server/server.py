import databases
from fastapi import FastAPI
from typing import List, Optional

import pipeline_orchestrator.server.model
from pipeline_orchestrator.server.config import DevConfig
import pipeline_orchestrator.tracking.schema
from pipeline_orchestrator.tracking.db import DbAccessor

config = DevConfig

database = databases.Database(config.DB_URL)

db_interface = DbAccessor(database)


app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {
        'Hello': 'World'
    }


@app.get("/pipeline", response_model=List[pipeline_orchestrator.server.model.Pipeline])
async def pipelines():
    return await db_interface.get_all_pipelines()


@app.post("/pipelines")
async def create_pipeline():
    return None


@app.get("/run_status", response_model=List[pipeline_orchestrator.server.model.AnalysisRun])
async def runs(state: Optional[str] = None):
    return await db_interface.get_analysis_runs(state)
