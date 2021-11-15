import pytest

from pipeline_orchestrator.tracking.schema import (
    Pipeline, Analysis, AnalysisRun, Event, Agent
)


@pytest.fixture
def minimum_data(sync_session):
    'Provides one of everything'

    print(type(sync_session))
    pipeline = Pipeline(
        user_id=1,
        repository_uri='pipeline-test.com',
        version='0.3.14'
    )
    analysis = Analysis(
        work_detector='script.py',
        state='READY',
        pipeline=pipeline
    )
    agent = Agent(
        name='local'
    )

    event = Event(
        agent=agent,
        change='Created'
    )
    runs = [AnalysisRun(
        analysis=analysis,
        job_descriptor='31401:4:1',
        state='READY',
        prefix='test-',
        events=[event]
    )]
    analysis.analysis_runs = runs

    sync_session.add_all([pipeline, analysis, agent, event])
    sync_session.add_all(runs)
    sync_session.commit()
    return sync_session
