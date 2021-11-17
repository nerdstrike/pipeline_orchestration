from fastapi import FastAPI, Depends
# also ApiRouter to get routes out of here

from starlette import status
from typing import List, Optional

from pipeline_orchestrator.version import __version__
from pipeline_orchestrator.server.model import (
    Pipeline, AnalysisRun, WorkRegistrationResult,
    WorkArray
)
from pipeline_orchestrator.tracking.db import get_DbAccessor

app = FastAPI()


@app.get("/")
async def root():
    return {
        'Hello': 'World',
        'Service': 'Pipeline Orchestrator',
        'Version': __version__
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
async def create_analysis_run(
    analysis_id: str,
    agent_id: str,
    work: WorkArray,
    db_interface=Depends(get_DbAccessor)
):
    # Some kind of validation?
    results = await db_interface.create_run(analysis_id, agent_id, work)
    return results


@app.put(
    '/{analysis_id}/claim_work',
    status_code=status.HTTP_200_OK,
    response_model=WorkArray
)
async def claim_analysis_run(
    analysis_id: str,
    agent_id: str,
    max_items: Optional[int] = 1,
    db_interface=Depends(get_DbAccessor)
):
    work = await db_interface.claim_runs(agent_id, analysis_id, max_items)
    print(work)
    return work
