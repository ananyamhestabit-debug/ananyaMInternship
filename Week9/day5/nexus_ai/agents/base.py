from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config import *

def create_agent(name, system_prompt):

    model = OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.3,
        model_info=MODEL_INFO,
    )

    return AssistantAgent(
        name=name,
        system_message=system_prompt,
        model_client=model,
    )