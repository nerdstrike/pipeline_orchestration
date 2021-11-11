import logging
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import List

from pipeline_orchestrator.server.config import DevConfig

from pipeline_orchestrator.tracking.schema import (
    Agent, Analysis, AnalysisRun, Pipeline
)

config = DevConfig
engine = create_async_engine(
    config.DB_URL, future=True
)
session_factory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


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

    async def create_run(self, analysis_id: str, agent_id: str, runs: List[object]):
        async with self.session.begin():
            # Now we have an AsyncSessionTransaction

            session = self.session
            agent = await session.execute(
                select(Agent)
                .where(agent_id=agent_id)
            ).scalar_one()
            analysis = await session.execute(
                select(Analysis)
                .where(analysis_id=analysis_id)
            ).scalar_one()
            # Check they exist and so on

            for run in runs:
                analysis_run = AnalysisRun(
                    agent=agent,
                    analysis=analysis,
                    job_descriptor='blurp'
                )
                session.add(analysis_run)
