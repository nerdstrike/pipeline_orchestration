import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import string

from pipeline_orchestrator.tracking.schema import (
    Pipeline, Agent, Analysis, AnalysisRun
)


def make_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


uri = 'sqlite:///test.db'

engine = create_engine(uri)
session_factory = sessionmaker(bind=engine)
session = session_factory()

for i in range(5):
    agent = Agent(name=str(i))
    session.add(agent)
session.commit()

# Make some pipelines
for i in range(1000):
    pipeline = Pipeline(
        repository_uri=make_random_string(8)
    )
    analysis = Analysis(
        pipeline=pipeline,
        state='READY'
    )
    runs = []
    for j in range(random.randrange(1, 5000)):
        run = AnalysisRun(
            analysis=analysis,
            job_descriptor=make_random_string(20),
            definition={
                'pipeline': pipeline.repository_uri,
                'run': make_random_string(20),
                'lane': random.randrange(13)
            },
            state='READY'
        )
        runs.append(run)

    session.add_all([pipeline, analysis])
    session.add_all(runs)
    session.commit()

session.close()
engine.dispose()
