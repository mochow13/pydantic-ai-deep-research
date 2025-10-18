import json

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from rich.prompt import Prompt

from config.console_config import console, success_style, error_style
from commons.models import Model
from commons.prompts import (
    research_planner_prompt,
    research_plan_user_feedback_prompt,
    research_topic_eligibility_prompt
)
from commons._types import ResearchPlan

class ResearchPlanner:
    
    def __init__(self):
        self.model = Model("litellm_proxy/cody::gpt-4o")
        self.mini_model = Model("litellm_proxy/cody::gpt-4o-mini")
    
    def evaluate_research_eligibility(self, topic: str) -> bool:
        agent = Agent(model=self.mini_model.getModel(), output_type=bool)
        prompt = research_topic_eligibility_prompt.format(research_topic=topic)

        with console.status("Evaluating research eligibility...", spinner="dots"):
            result = agent.run_sync(prompt)

        return result.output
    
    def create_initial_research_plan(self, research_topic: str, message_history: list[ModelMessage]) -> tuple[bool, ResearchPlan]:
        agent = Agent(model=self.model.getModel(), output_type=ResearchPlan)
        
        try:
            initial_prompt = research_planner_prompt.format(research_topic=research_topic)
            
            with console.status("Generating research plan...", spinner="dots"):
                result = agent.run_sync(initial_prompt, message_history=message_history)
            
            console.print("\n📜 Research Plan:", style=success_style)
            console.print(json.dumps(result.output.model_dump(), indent=2))
            message_history.extend(result.all_messages())
            return True, result.output
            
        except Exception as e:
            console.print(f"\n❌ Error creating initial plan: {e}", style=error_style)
            return False, None

    def finalize_plan_on_feedback(self, initial_research_plan: ResearchPlan,
                                  message_history: list[ModelMessage]) -> ResearchPlan | None:
        final_research_plan = initial_research_plan
        agent = Agent(model=self.model.getModel(), output_type=ResearchPlan)
        
        while True:
            user_feedback = Prompt.ask("\n💡 Your feedback on the plan (or 'start/ok/begin' to begin)")
            
            if user_feedback.lower() in ['quit', 'exit', 'q']:
                console.print("\nGoodbye!")
                break
            
            if user_feedback.lower() in ['start', 'begin', 'go', 'ok', 'good', 'looks good']:
                return final_research_plan
            
            try:
                refinement_prompt = research_plan_user_feedback_prompt.format(user_feedback=user_feedback)
                
                with console.status("Refining research plan...", spinner="dots"):
                    result = agent.run_sync(refinement_prompt, message_history=message_history)
                
                console.print("\n📝 Updated Research Plan:", style=success_style)
                console.print(json.dumps(result.output.model_dump(), indent=2))
                message_history.extend(result.all_messages())
                final_research_plan = result.output
                
            except Exception as e:
                console.print(f"\nError: {e}", style=error_style)
                console.print("Please try again or type 'quit' to exit.")
        
        return None
    
    def create_research_plan(self, research_topic: str) -> ResearchPlan | None:
        if not self.evaluate_research_eligibility(research_topic):
            return None
        
        console.print(f"✅ Research topic \"{research_topic}\" is eligible for research!", style=success_style)
        
        message_history: list[ModelMessage] = []
        is_success, initial_research_plan = self.create_initial_research_plan(research_topic, message_history)
        
        if not is_success:
            console.print("\n❌ Error creating initial plan.", style=error_style)
            return None
        
        final_research_plan = self.finalize_plan_on_feedback(initial_research_plan, message_history)
        
        return final_research_plan
