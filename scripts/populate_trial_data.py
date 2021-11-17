from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pipeline_orchestrator.tracking.schema import Pipeline, Agent, Analysis

# Insert engine selection and credential loading... e.g. engine_from_config()

engine = create_engine('sqlite:///test.db')
session_factory = sessionmaker(bind=engine)
session = session_factory()

pipeline = Pipeline(repository_uri='https://pipeline.com', version='3.1.4')
analysis = Analysis(pipeline=pipeline)

session.add(pipeline)
session.add(analysis)

session.add(
    Agent(name='localhost')
)

session.commit()
