import pipeline_orchestrator.tracking.schema
import sqlalchemy

# Insert engine selection and credential loading... e.g. engine_from_config()
engine = sqlalchemy.create_engine('sqlite:///test.db')

pipeline_orchestrator.tracking.schema.Base.metadata.create_all(engine)
