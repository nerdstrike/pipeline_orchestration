import pydantic
from typing import Any, Dict, List


class Pipeline(pydantic.BaseModel):
    pipeline_id: str = pydantic.Field(
        None, title='Unique identifier for a pipeline/version combination'
    )
    repository_uri: str = pydantic.Field(
        None, title='URI for retrieving the code for the pipeline'
    )
    version: str = pydantic.Field(
        None, title='The version string for the pipeline'
    )

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'pipeline_id': '1',
                'repository_uri': 'https://pipeline.example/code.git',
                'version': '1.2.3'
            }
        }


class AnalysisRun(pydantic.BaseModel):
    job_descriptor: str
    state: str

    class Config:
        orm_mode = True


class Work(pydantic.BaseModel):
    definition: Dict[str, Any] = pydantic.Field(
        None, title='Defining the unique properties for this work'
    )
    info: Dict[str, Any] = pydantic.Field(
        None, title='Supporting information for this particular unit of work'
    )

    class Config:
        schema_extra = {
            'example': {
                'definition': {
                    'run': 1234,
                    'lane': 5,
                    'tag_index': 6
                },
                'info': {
                    'species': 'Homo Sapiens',
                    'library_type': 'cell partitioned RNA expression'
                }
            }
        }


class WorkRegistrationResult(pydantic.BaseModel):
    created: List[Work] = pydantic.Field(
        [], title='A list of work units created in the operation'
    )
    errored: List[str] = pydantic.Field(
        [], title='Failed items that were not registered for some reason'
    )
    preexisting: List[Work] = pydantic.Field(
        [], title='Items that were not created because they already exist'
    )


class WorkArray(pydantic.BaseModel):
    __root__: List[Work] = pydantic.Field(
        [], title='A list of Work descriptions to be run'
    )
    # These are necessary because a bare list in JSON is
    # uncommon and the handling in fastapi/pydantic is
    # not available by default

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
