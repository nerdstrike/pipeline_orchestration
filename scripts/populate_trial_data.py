from pipeline_orchestrator.tracking.schema import connect_db, Pipeline, Agent

# Insert engine selection and credential loading... e.g. engine_from_config()

session = connect_db({'url': 'sqlite:///test.db'})
session.add(
    Pipeline(repository_uri='https://pipeline.com', version='3.1.4')
)

session.add(
    Agent(name='localhost')
)

session.commit()
