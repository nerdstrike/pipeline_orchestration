from typing import Optional

from fastapi import FastAPI
from typing import List

import pipeline_orchestrator.server.model
from pipeline_orchestrator.server.config import DevConfig
import pipeline_orchestrator.tracking.schema

config = DevConfig

db_session = pipeline_orchestrator.tracking.schema.connect_db({
    'url': config.DB_URL,
    'future': True,
    'check_same_thread': config.SAME_THREAD
})


app = FastAPI()


@app.get("/", response_model=List[pipeline_orchestrator.server.model.Pipeline])
async def root():
    pipeline_data = db_session.query(
        pipeline_orchestrator.tracking.schema.Pipeline
    ).all()

    return pipeline_data


@app.get("/run_status", response_model=List[pipeline_orchestrator.server.model.AnalysisRun])
async def runs(state: Optional[str] = None):
    if state:
        runs = db_session.query(
            pipeline_orchestrator.tracking.schema.AnalysisRun
        ).filter_by(
            state=state
        ).all()
    else:
        runs = db_session.query(
            pipeline_orchestrator.tracking.schema.AnalysisRun
        ).all()

    return runs
