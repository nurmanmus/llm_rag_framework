from llm.schemas import Config, HuggingFaceConfig

# this is for ollama and chatgpt
config_dict = {
    "model": "llama2:7b-chat",
    "temperature": 0.9,
}

llm_config = Config(**config_dict)

# this is for huggingface
huggingface_config_dict = {
    "repo_id": "EleutherAI/gpt-neo-2.7B",
    "model_kwargs": {
        "temperature": 0.9,
        "max_length": 128,
    },
}


# mistral_config_dict
mistral_config_dict = {
    "repo_id": "mistralai/Mistral-7B-Instruct-v0.2",
    "model_kwargs": {
        "temperature": 0.9,
        "max_length": 2024,
    },
}


# mixtral_config_dict
mixtral_config_dict = {
    "repo_id": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "model_kwargs": {
        "temperature": 0.9,
        "max_length": 1024,
    },
}

mistral_config = HuggingFaceConfig(**mistral_config_dict)
mixtral_config = HuggingFaceConfig(**mixtral_config_dict)
