#!/usr/bin/env python3
# A daemomisable (not yet) process that polls the orchestration service
# for work it can execute, then selects a batch of runs and executes
# them.

import subprocess

from pipeline_orchestrator.tracking.schema import Pipeline, Analysis,\
     AnalysisRun, Event, Agent, connect_db
from sqlalchemy import select

orch_session = connect_db({
    'url': 'sqlite:///test.db'
})

pipeline_uri = 'https://pipeline.com'
version = '3.1.4'

# Find myself

orm_agent = orch_session.execute(
    select(Agent).filter(Agent.name == 'localhost')
).scalars().one()

# See what's available for the particular analysis
claimable_jobs = orch_session.execute(
    select(AnalysisRun).
    join(Analysis).
    join(Pipeline).
    filter(AnalysisRun.state == 'READY').
    filter(Pipeline.repository_uri == pipeline_uri).
    limit(10)
).scalars().all()

for job in claimable_jobs:
    job.state = 'CLAIMED'
    event = Event(analysis_run=job, set_by=orm_agent.agent_id, change='Job taken')
    orch_session.add(event)
    print(job.job_descriptor)

orch_session.commit()

for job in claimable_jobs:
    # mark each job as running and create an event log of it
    job.state = 'RUNNING'
    event = Event(analysis_run=job, set_by=orm_agent.agent_id, change='Started job')
    orch_session.add(event)
    orch_session.commit()
    # run the set of selected jobs
    proc = subprocess.run(
        [
            'pipeline/toy1/pipeline.py',
            '--file',
            job.analysis.pipeline.repository_uri,
            '--work_dir',
            '/tmp'
        ],
        capture_output=True
    )
    # print(proc.stdout.decode())
    # print(proc.stderr.decode())
    proc.check_returncode()
    # Do more around check_returncode() to mark failures
    job.state = 'DONE'
    event = Event(analysis_run=job, set_by=orm_agent.agent_id, change='Finished job')
    orch_session.add(event)
    orch_session.commit()
