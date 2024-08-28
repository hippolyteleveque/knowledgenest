import os


def load_env_var(var_name: str) -> str:
    """Raise errror if one of the necessary values has not been provided"""
    val = os.getenv(var_name)
    if not val:
        raise ValueError(
            f"Knowledgenest requires {var_name} to be defined in the environment"
        )
    return val


OPENAI_API_KEY = load_env_var("OPENAI_API_KEY")
OPENAI_LLM_MODEL = "gpt-4o-mini"
MISTRAL_API_KEY = load_env_var("MISTRAL_API_KEY")
MISTRAL_EMBEDDING_MODEL = "mistral-embed"
MISTRAL_LLM_MODEL = "open-mistral-nemo"
ANTHTROPIC_API_KEY = load_env_var("ANTHROPIC_API_KEY")
PINECONE_API_KEY = load_env_var("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "knowledgenest"
ANTHROPIC_LLM_MODEL = "claude-3-haiku-20240307"
