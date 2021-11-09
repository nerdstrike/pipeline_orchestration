import logging
from sqlalchemy import select

from pipeline_orchestrator.tracking.schema import Pipeline, AnalysisRun


class DbAccessor:
    '''
    A convenience
    '''

    logger = logging.getLogger(__name__)

    def __init__(self, database):
        self.database = database

    async def get_all_pipelines(self):
        pipelines = await self.database.fetch_all(
            query=select(Pipeline)
        )

        return pipelines

    async def get_analysis_runs(self, state):
        if (state):
            analysis_runs = await self.database.fetch_all(
                select(AnalysisRun)
                .filter(state=state)
            )
        else:
            analysis_runs = await self.database.fetch_all(
                select(AnalysisRun)
            )

        return analysis_runs
