import os

#loads prompts
def load_prompt(file_name):
    base_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_path, "prompts", file_name)

    with open(path, "r") as f:
        return f.read()