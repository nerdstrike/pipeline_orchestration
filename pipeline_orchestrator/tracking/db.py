import logging
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import List, Optional, Dict

from pipeline_orchestrator.server.config import DevConfig

from pipeline_orchestrator.tracking.schema import (
    Agent, Analysis, AnalysisRun, Pipeline
)

from pipeline_orchestrator.server.model import WorkArray, Work

config = DevConfig
engine = create_async_engine(
    config.DB_URL, future=True
)
session_factory = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_DbAccessor():
    'Provides a hook for fastapi to Depend on a live session on each route'
    async with session_factory() as session:
        async with session.begin():
            yield DbAccessor(session)


class DbAccessor:
    '''
    A convenience
    '''

    logger = logging.getLogger(__name__)

    def __init__(self, session):
        self.session = session

    async def get_all_pipelines(self):
        pipelines = await self.session.execute(
            select(Pipeline)
        )

        return pipelines.scalars().all()

    async def get_analysis_runs(self, state: str):
        if (state):
            analysis_runs = await self.session.execute(
                select(AnalysisRun)
                .filter(state=state)
            )
        else:
            analysis_runs = await self.session.execute(
                select(AnalysisRun)
            )

        return analysis_runs.scalars().all()

    async def create_run(self, analysis_id: str, agent_id: str, runs: WorkArray):

        session = self.session
        agent_result = await session.execute(
            select(Agent)
            .filter_by(agent_id=agent_id)
        )
        agent = agent_result.scalar_one()
        analysis_result = await session.execute(
            select(Analysis)
            .filter_by(analysis_id=analysis_id)
        )
        analysis = analysis_result.scalar_one()
        # Check they exist and so on

        for run in runs:
            definition = create_descriptor(run.definition)
            analysis_run = AnalysisRun(
                agent=agent,
                analysis=analysis,
                job_descriptor=definition,
                state='READY'
            )
            session.add(analysis_run)

        await session.commit()
        # Error handling to follow
        return {
            'created': list(runs),
            'errored': [],
            'preexisting': []
        }

    async def claim_run(self, agent_id: int, analysis_id: int, claim_limit: Optional[int] = 1):
        session = self.session

        agent = await session.execute(
            select(Agent)
            .where(agent_id=agent_id)
        ).scalar_one()

        potential_runs = await session.execute(
            select(AnalysisRun)
            .where(analysis=analysis_id)
            .filter_by(state='READY')
        ).limit(claim_limit)

        runs = potential_runs.scalars().all()
        for run in runs:
            run.claimed_by(agent)
            run.state('CLAIMED')

        return runs


def create_descriptor(definition: Dict):
    descriptor = ''
    for thing in ('run', 'lane', 'tag_index'):
        descriptor = ':'.join([descriptor, str(definition[thing])])
    return descriptor
