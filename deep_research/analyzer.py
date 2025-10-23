from pydantic_ai import Agent, WebSearchTool
from pydantic_ai.messages import ModelMessage

from config.console_config import console
from commons.models import Model
from config.model_config import ANALYZER_MODEL
from commons.prompts import analyzer_prompt
from commons._types import ResearchStepResult, ResearchStep

class ResearchAnalyst:
    def __init__(self):
        self.model = Model(ANALYZER_MODEL)
        self.agent = Agent(model = self.model.getModel(), output_type=ResearchStepResult, builtin_tools=[WebSearchTool()])

    def execute_single_step(self, topic: str, step: ResearchStep, message_history: list[ModelMessage]):
        prompt = analyzer_prompt.format(topic=topic, step=step)

        with console.status("Running analysis for research steps...", spinner="dots10"):
            result = self.agent.run_sync(prompt, message_history=message_history)
        
        return result

    def run_research_analysis(self, topic: str, steps: list[ResearchStep]) -> list[ResearchStepResult]:
        analysis = []
        message_history: list[ModelMessage] = []
        for step in steps:
            result = self.execute_single_step(topic, step, message_history)
            analysis.append(result.output)
            message_history.extend(result.all_messages())

        return analysis
