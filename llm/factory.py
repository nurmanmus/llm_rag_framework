from abc import ABC, abstractmethod

from langchain.chat_models import ChatOllama
from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain.llms.huggingface_hub import HuggingFaceHub
from langchain.llms.ollama import Ollama

from .enums import LLMType


class AbstractLLM(ABC):
    @abstractmethod
    def create(self):
        ...


class ChatOllamaLLM(AbstractLLM):
    def create(self, config):
        return ChatOllama(model=config.model, temperature=config.temperature)


class HuggingFaceHubLLM(AbstractLLM):
    def create(self, config):
        return HuggingFaceHub(
            repo_id=config.repo_id,
            model_kwargs=config.model_kwargs,
        )


class HuggingFaceEndpointLLM(AbstractLLM):
    def create(self, config):
        return HuggingFaceEndpoint(
            endpoint_url=config.endpoint_url,
            task=config.task,
            huggingfacehub_api_token=config.huggingfacehub_api_token,
        )


class OllamaLLM(AbstractLLM):
    def create(self, config):
        return Ollama(model=config.model, temperature=config.temperature)


class LLMFactory:
    _llm_map = {
        LLMType.CHAT_OLLAMA: ChatOllamaLLM,
        LLMType.HUGGINGFACE_API: HuggingFaceHubLLM,
        LLMType.HUGGINGFACE_ENDPOINT: HuggingFaceEndpointLLM,
        LLMType.OLLAMA: OllamaLLM,
    }

    @staticmethod
    def create_factory(llm_type, config):
        try:
            return LLMFactory._llm_map[llm_type]().create(config)
        except KeyError:
            raise ValueError(f"Invalid llm type: {llm_type}")
