import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_scoped_session
)
from typing import Optional, Dict, List

from pipeline_orchestrator.tracking.schema import (
    Agent, Analysis, AnalysisRun, Pipeline, Event
)

from pipeline_orchestrator.server.model import Work
from pipeline_orchestrator.server.config import DevConfig

config = DevConfig

engine = create_async_engine(
    config.DB_URL, future=True, pool_size=4
)

session_factory = async_scoped_session(
    sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    ),
    scopefunc=asyncio.current_task
)


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

    async def create_run(self, analysis_id: str, agent_id: str, runs: List[Work]):

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
                definition=run,
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

    async def claim_runs(
        self, agent_id: int, analysis_id: int, claim_limit: Optional[int] = 1
    ):
        session = self.session

        agent_result = await session.execute(
            select(Agent)
            .filter_by(agent_id=agent_id)
        )
        agent = agent_result.scalar_one()

        try:
            to_claim = await session.execute(
                select(AnalysisRun)
                .filter_by(analysis_id=analysis_id)
                .filter_by(state='READY')
                # .filter_by(claimed_by=None) Goes faster without this redundant safety
                .with_for_update()
                .limit(claim_limit)
                .execution_options(populate_existing=True)
            )
        except NoResultFound:
            print("Whoopsie. No runs in READY state")
            return []

        runs = to_claim.scalars().all()
        # savepoint = session.begin_nested()
        try:
            for run in runs:
                run.agent = agent
                run.state = 'CLAIMED'
                event = Event(change='Run claimed', agent=agent, analysis_run=run)
                session.add(event)

            await session.commit()
        except IntegrityError as e:
            print(e)
            session.rollback()

        work = []
        for run in runs:
            work.append({'definition': run.definition, 'info': None})
        return work


def create_descriptor(definition: Dict):
    'Get rid of this. This is the responsibility of the "work finder"'
    descriptor = ''
    for thing in ('run', 'lane', 'tag_index'):
        descriptor = ':'.join([descriptor, str(definition[thing])])
    return descriptor
