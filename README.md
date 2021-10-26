# Pipeline Orchestration tech demo

For when pipelines must be run following arbitrary triggering conditions, and their progress must be tracked. Python 3.8+

**pipeline_orchestrator** defines a database __tracking__ schema as well as a very basic __fastapi__ web server.
**pipeline** will collect example pipelines that this orchestration service might manage.

    pipeline/toy1/workfinder.py must have access to ml-warehouse in order to generate work orders. It does so using the NPG python ml-warehouse library.
    Before running, set `MLWH_URI` to something resembling `mysql+pymysql://${USER}:${PASS}@${MIRROR_MLWAREHOUSE}:${PORT}/mlwhd_mlwarehouse_proddata`
