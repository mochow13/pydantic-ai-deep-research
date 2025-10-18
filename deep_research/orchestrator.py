import json

from rich.prompt import Prompt
from commons._types import ResearchPlan
from config.console_config import console, success_style, error_style
from deep_research.planner import ResearchPlanner
from deep_research.analyzer import ResearchAnalyst

class ResearchOrchestrator:
    
    def __init__(self):
        self.planner = ResearchPlanner()
        self.analyst = ResearchAnalyst()
    
    def _get_valid_research_plan(self):
        while True:
            research_topic = Prompt.ask("\n🔬 Enter your research topic")

            if research_topic.lower() in ['quit', 'exit', 'q']:
                console.print("\n👋 Goodbye!")
                return None

            final_research_plan = self.planner.create_research_plan(research_topic)
            
            if final_research_plan is None:
                console.print("\n🚫 Sorry, the topic is not eligible for research. Try again...", style=error_style)
                continue
            
            console.print("\n🚀 Final Research Plan:", style=success_style)
            console.print(json.dumps(final_research_plan.model_dump(), indent=2))

            return final_research_plan

    def _execute_analysis(self, plan: ResearchPlan):
        analysis = self.analyst.run_research_analysis(plan.refined_topic, plan.steps)
        console.print("📘 Research analysis:", style=success_style)

        for step_result in analysis:
            console.print(json.dumps(step_result.model_dump(), indent=2))

        return analysis

    def run_research_session(self) -> None:
        plan = self._get_valid_research_plan()
        
        if plan is None:
            return
        
        analysis = self._execute_analysis(plan)
