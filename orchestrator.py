import json

from rich.prompt import Prompt
from console_config import console, success_style, error_style
from planner import ResearchPlanner

class ResearchOrchestrator:
    
    def __init__(self):
        self.planner = ResearchPlanner()
    
    def run_research_session(self) -> None:
        while True:
            research_topic = Prompt.ask("\n🔬 Enter your research topic")

            if research_topic.lower() in ['quit', 'exit', 'q']:
                console.print("\n👋 Goodbye!")
                return

            final_research_plan = self.planner.create_research_plan(research_topic)
            
            if final_research_plan is None:
                console.print("\n🚫 Sorry, the topic is not eligible for research. Try again...", style=error_style)
                continue
            
            console.print("\n🚀 Final Research Plan:", style=success_style)
            console.print(json.dumps(final_research_plan.model_dump(), indent=2))
            break
