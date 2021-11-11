from fastapi import FastAPI, Depends
# also ApiRouter to get routes out of here
from starlette import status
from typing import List, Optional, Dict

from pipeline_orchestrator.server.model import Pipeline, AnalysisRun, WorkRegistrationResult
from pipeline_orchestrator.tracking.db import get_DbAccessor

app = FastAPI()


# @app.on_event('startup')
# async def startup():
#     await engine.connect()


# @app.on_event('shutdown')
# async def shutdown():
#     await engine.dispose()


@app.get("/")
async def root():
    return {
        'Hello': 'World'
    }


@app.get("/pipeline", response_model=List[Pipeline])
async def get_pipelines(db_interface=Depends(get_DbAccessor)):
    return await db_interface.get_all_pipelines()


@app.post("/pipeline")
async def create_pipeline():
    return None


@app.get("/run_status", response_model=List[AnalysisRun])
async def runs(state: Optional[str] = None, db_interface=Depends(get_DbAccessor)):
    return await db_interface.get_analysis_runs(state)


@app.post(
    '/{analysis_id}/register_work',
    status_code=status.HTTP_201_CREATED,
    response_model=WorkRegistrationResult
)
async def create_analysis_run(analysis_id: str, body: Dict, agent_id: Optional[str], db_interface=Depends(get_DbAccessor)):
    runs = [run for run in body]
    # Some kind of validation?
    await db_interface.create_work(analysis_id, agent_id, runs)
