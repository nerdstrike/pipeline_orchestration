import databases
from fastapi import FastAPI
from starlette import status
from typing import List, Optional, Dict

from pipeline_orchestrator.server.config import DevConfig
from pipeline_orchestrator.server.model import Pipeline, AnalysisRun, WorkRegistrationResult
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


@app.get("/pipeline", response_model=List[Pipeline])
async def pipelines():
    return await db_interface.get_all_pipelines()


@app.post("/pipelines")
async def create_pipeline():
    return None


@app.get("/run_status", response_model=List[AnalysisRun])
async def runs(state: Optional[str] = None):
    return await db_interface.get_analysis_runs(state)


@app.post(
    '/{analysis_id}/register_work',
    status_code=status.HTTP_201_CREATED,
    response_model=WorkRegistrationResult
)
async def create_analysis_run(analysis_id: str, body: Dict, agent_id: Optional[str]):
    runs = [run for run in body]
    # Some kind of validation?
    await db_interface.create_work(analysis_id, agent_id, runs)
