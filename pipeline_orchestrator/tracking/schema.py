import sqlalchemy
from sqlalchemy import (
    Column, ForeignKey, Integer, String, DateTime, UniqueConstraint, PickleType
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Pipeline(Base):
    '''
    A black box of science
    '''
    __tablename__ = 'pipeline'
    pipeline_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    repository_uri = Column(String)
    version = Column(String)

    UniqueConstraint('repository_uri', 'version', name='unique_pipeline')

    analyses = relationship('Analysis', back_populates='pipeline')


class Analysis(Base):
    '''
    A parameterised Pipeline with a specific set of criteria
    that trigger AnalysisRuns.
    '''
    __tablename__ = 'analysis'
    analysis_id = Column(Integer, primary_key=True, autoincrement=True)
    pipeline_id = Column(Integer, ForeignKey('pipeline.pipeline_id'))
    work_detector = Column(String)
    outcome = Column(String)
    state = Column(String)

    analysis_runs = relationship(
        'AnalysisRun', back_populates='analysis'
    )
    pipeline = relationship(
        'Pipeline', back_populates='analyses'
    )


class AnalysisRun(Base):
    '''
    A unique combination of inputs for an Analysis
    '''
    __tablename__ = 'analysis_run'
    run_id = Column(Integer, primary_key=True, autoincrement=True)
    claimed_by = Column(Integer, ForeignKey('agent.agent_id'))
    analysis_id = Column(Integer, ForeignKey('analysis.analysis_id'))
    job_descriptor = Column(String, unique=True)
    # definition is the serialisation of Dict representing the JSON
    # provided by the workflow - we don't want to get into serialising
    # and deserialising from job_descriptor above, so we keep the original
    definition = Column(PickleType)
    state = Column(String)
    # prefix is a special property for uniquifying folder names
    # or LSF job names and so on.
    prefix = Column(String)

    UniqueConstraint('analysis_id', 'job_descriptor', name='unique_work')
    # sample = Column(Integer)
    # study = Column(Integer)
    # run_id = Column(Integer)
    # lane = Column(Integer) / movie / well
    # plex = Column(Integer)

    analysis = relationship(
        'Analysis', back_populates='analysis_runs'
    )
    events = relationship(
        'Event', back_populates='analysis_run'
    )
    agent = relationship(
        'Agent', back_populates='analysis_runs'
    )


class Event(Base):
    '''
    A sequence of time-stamped state changes for each AnalysisRun for
    reporting and metrics purposes.
    '''
    __tablename__ = 'event'
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    analysis_run_id = Column(Integer, ForeignKey('analysis_run.run_id'))
    time = Column(DateTime, default=sqlalchemy.sql.functions.now())
    set_by = Column(Integer, ForeignKey('agent.agent_id'))
    change = Column(String)

    analysis_run = relationship(
        'AnalysisRun'
    )

    agent = relationship(
        'Agent', back_populates='events'
    )


class Agent(Base):
    '''
    An autonomous client that can take work units
    '''
    __tablename__ = 'agent'
    agent_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    analysis_runs = relationship(
        'AnalysisRun'
    )
    events = relationship(
        'Event', back_populates='agent'
    )
