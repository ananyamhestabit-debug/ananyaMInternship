def get_llm_config():
    import os

    model_name = os.getenv("MODEL_NAME", "tinyllama")

    return {
        "config_list": [
            {
                "model": model_name,
                "base_url": "http://localhost:11434/v1",
                "api_key": "NULL"
            }
        ],
        "temperature": 0.3,
    }