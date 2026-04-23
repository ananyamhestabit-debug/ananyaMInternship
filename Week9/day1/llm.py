import requests  #python library to make http calls 

# it is a bridge between code and the model
def call_llm(messages, model="mistral"):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": model,
            "messages": messages,
            "stream": False  #not token by token streaming , wait or full response
        }
    )

    return response.json()["message"]["content"]  #convert response to dictionary, access message object and actual text output