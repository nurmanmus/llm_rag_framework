from enum import Enum, auto


class LLMType(Enum):
    CHAT_OLLAMA = auto()
    HUGGINGFACE_API = auto()
    HUGGINGFACE_ENDPOINT = auto()
    OLLAMA = auto()
