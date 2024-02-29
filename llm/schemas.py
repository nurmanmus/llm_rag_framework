from langchain_core.pydantic_v1 import BaseModel as LangchainBaseModel
from pydantic import BaseModel


class Question(LangchainBaseModel):
    __root__: str


class Config(BaseModel):
    model: str
    temperature: float = 0.9


class HuggingFaceConfig(BaseModel):
    repo_id: str
    model_kwargs: dict


class HuggingFaceEndpointConfig(BaseModel):
    endpoint_url: str
    huggingfacehub_api_token: str
    task: str = "text-generation"


class LLMInput(BaseModel):
    query: str


class LLMOutput(BaseModel):
    query: str
    text: str
