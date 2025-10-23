from pydantic_ai import Agent

from config.console_config import console
from commons.models import Model
from config.model_config import SYNTHESIZER_MODEL
from commons.prompts import synthesizer_prompt

class ResearchSynthesizer:
    def __init__(self):
        self.model = Model(SYNTHESIZER_MODEL)
        self.agent = Agent(model = self.model.getModel())

    def synthesize_report(self, topic, objectives, key_questions, analysis):
        prompt = synthesizer_prompt.format(topic=topic, objectives=objectives, key_questions=key_questions, analysis=analysis)
        
        with console.status("Synthesizing research report...", spinner="dots2"):
            result = self.agent.run_sync(prompt)

        return result.output
