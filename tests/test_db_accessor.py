from sqlalchemy import select
from pipeline_orchestrator.tracking.schema import Pipeline


def test_nothing(minimum_data):
    'Show that test DB is created, populated and cleaned up'

    pipelines = minimum_data.execute(
        select(Pipeline)
    ).scalars().all()

    assert len(pipelines) == 1
