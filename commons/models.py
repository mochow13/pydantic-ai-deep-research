from pydantic_ai_litellm import LiteLLMModel

class Model:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.api_base = "http://localhost:4000"
        self.api_key = "noop"

    def getModel(self):
        return LiteLLMModel(
            model_name=self.model_name,
            api_base=self.api_base,
            api_key=self.api_key
        )