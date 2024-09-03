import os
from typing import Dict, ClassVar, Optional

from pydantic import BaseModel


def load_env_var(var_name: str) -> str:
    """Raise errror if one of the necessary values has not been provided"""
    val = os.getenv(var_name)
    if not val:
        raise ValueError(
            f"Knowledgenest requires {var_name} to be defined in the environment"
        )
    return val


def setenv(var_name: str, value: str) -> str:
    """Set the variable to the value and returns it"""
    os.environ[var_name] = value
    return value


def init_config() -> Dict[str, str]:
    environment = load_env_var("ENVIRONMENT")
    pc_idx_name = (
        "knowledgenest-dev" if environment == "DEVELOPMENT" else "knowledegenest-prod"
    )
    return {
        "OPENAI_API_KEY": load_env_var("OPENAI_API_KEY"),
        "OPENAI_LLM_MODEL": "gpt-4o-mini",
        "MISTRAL_API_KEY": load_env_var("MISTRAL_API_KEY"),
        "MISTRAL_EMBEDDING_MODEL": "mistral-embed",
        "MISTRAL_LLM_MODEL": "open-mistral-nemo",
        "ANTHROPIC_API_KEY": load_env_var("ANTHROPIC_API_KEY"),
        "PINECONE_API_KEY": load_env_var("PINECONE_API_KEY"),
        "PINECONE_INDEX_NAME": pc_idx_name,
        "ANTHROPIC_LLM_MODEL": "claude-3-haiku-20240307",
        "LANGCHAIN_API_KEY": load_env_var("LANGCHAIN_API_KEY"),
        "LANGCHAIN_PROJECT": load_env_var("LANGCHAIN_PROJECT"),
        "LANGCHAIN_TRACING_V2": setenv("LANGCHAIN_TRACING_V2", "true"),
        "LANGCHAIN_ENDPOINT": setenv(
            "LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"
        ),
    }


class Config(BaseModel):
    OPENAI_API_KEY: str
    OPENAI_LLM_MODEL: str = "gpt-4o-mini"
    MISTRAL_API_KEY: str
    MISTRAL_EMBEDDING_MODEL: str = "mistral-embed"
    MISTRAL_LLM_MODEL: str = "open-mistral-nemo"
    ANTHROPIC_API_KEY: str
    ANTHROPIC_LLM_MODEL: str
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str
    LANGCHAIN_API_KEY: str
    LANGCHAIN_PROJECT: str
    LANGCHAIN_TRACING_V2: str
    LANGCHAIN_ENDPOINT: str

    _instance: ClassVar[Optional["Config"]] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls(**init_config())
        return cls._instance


config: Config = Config.get_instance()
