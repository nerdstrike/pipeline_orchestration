import pydantic

# FastAPI stuff


class Pipeline(pydantic.BaseModel):
    id: str
    repository_uri: str = pydantic.Field(
        None, title="URI for retrieving the code for the pipeline"
    )
    version: str

    class Config:
        orm_mode = True
