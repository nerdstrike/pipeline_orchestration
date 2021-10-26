#!/usr/bin/env python3
# Finds things to do and logs them with the backend
# Looks for samples made for the ToL project and generates
# an Analysis run per PacBio run

import ml_warehouse
from ml_warehouse.ml_warehouse_schema import Study, PacBioRun, PacBioProductMetrics, PacBioRunWellMetrics

from pipeline_orchestrator.tracking.schema import Pipeline, Analysis, AnalysisRun, Event, connect_db


# Query the ml-warehouse for stuff.
session = ml_warehouse.get_wh_session()

orch_session = connect_db({
    'url': 'sqlite:///test.db'
})

pipeline_uri = 'https://pipeline.com'
version = '3.1.4'


def make_unique(study, run):
    '''
    Combines properties of a study and run to make a unique identifier for
    each piece of discrete work
    '''
    # I suppose well_label is redundant with the unique id_pac_bio_tmp
    # Official uniqueness is study+movie_name+well
    return f'{study.id_study_tmp}:{run.id_pac_bio_tmp}:{run.well_label}'


def register_analysis(db_session):
    db_pipe = db_session.query(Pipeline).\
        filter_by(repository_uri=pipeline_uri).\
        filter_by(version=version).\
        one()
    return Analysis(pipeline=db_pipe, state='READY')


def register_run(db_session, study, run, analysis):
    '''
    Accepts a sqlalchemy PacBioRun object and creates jobs in the
    orchestration service DB.
    '''

    job_descriptor = make_unique(study, run)
    # Find the pipeline

    # Weird - the new syntax doesn't work seemingly because of the warehouse
    # API being active.
    # db_pipe = db_session.execute(
    #     select(Pipeline).
    #         filter_by(repository_uri=pipeline_uri).
    #         filter_by(version=version)
    # ).scalar_one()

    # This fails if there isn't a one() to return
    db_pipe = db_session.query(Pipeline).\
        filter_by(repository_uri=pipeline_uri).\
        filter_by(version=version).\
        one()

    print(job_descriptor)
    print(db_pipe.repository_uri)

    # create a run in AnalysisRun
    db_session.add(AnalysisRun(
        analysis=analysis,
        job_descriptor=job_descriptor,
        state='READY'
    ))


analysis = register_analysis(orch_session)

studies = session.query(Study).\
            join(PacBioRun).\
            filter(Study.name.like('ToL%')).\
            all()

for study in studies:
    print(study.name)
    for run in study.pac_bio_run:
        print(run.well_label)
        register_run(orch_session, study, run, analysis)
    orch_session.commit()
