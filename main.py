import json

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from rich.prompt import Prompt
from rich.console import Console
from rich.style import Style
from models import Model

from prompts import (
    research_planner_prompt,
    research_plan_user_feedback_prompt,
    research_topic_eligibility_prompt
)
from _types import ResearchPlan

console = Console()
welcome_style = Style(color="yellow", bold=True)
success_style = Style(color="green", bold=True)
error_style = Style(color="red")

def log_initial_message():
    console.print("🎤 Welcome to the Research Planning Assistant!", style=welcome_style)
    console.print("Please provide a research topic and I'll create a research plan for you.", style=welcome_style)
    console.print("You can then provide feedback to refine the plan until you're satisfied.", style=welcome_style)
    console.print("Type 'quit' or 'exit' to end, or 'start research' when ready to begin.", style=welcome_style)
    console.print("-" * 70, style=welcome_style)

def create_initial_research_plan(research_topic: str, message_history: list[ModelMessage]) -> tuple[bool, ResearchPlan]:
    """Create the initial research plan and return True if successful, False otherwise."""

    # For research planning, we are using a larger model
    model = Model("litellm_proxy/cody::gpt-4o")
    agent = Agent(model=model.getModel(), output_type=ResearchPlan)
    
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


def finalize_plan_on_feedback(initial_research_plan: ResearchPlan,
                              message_history: list[ModelMessage]) -> ResearchPlan | None:
    """Handle the feedback and refinement loop for the research plan."""

    final_research_plan = initial_research_plan
    model = Model("litellm_proxy/cody::gpt-4o")
    agent = Agent(model=model.getModel(), output_type=ResearchPlan)
    
    while True:
        user_feedback = Prompt.ask("\n💡 Your feedback on the plan (or 'start research' to begin)")
        
        if user_feedback.lower() in ['quit', 'exit', 'q']:
            console.print("\nGoodbye!")
            break
        
        if user_feedback.lower() == 'start research':
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

def evaluate_research_eligibility(topic: str) -> bool:
    """
    Evaluate if the research topic is eligible for research.
    We can use a small LLM to determine if the topic is eligible for research.
    """

    model = Model("litellm_proxy/cody::gpt-4o-mini")
    agent = Agent(model=model.getModel(), output_type=bool)
    prompt = research_topic_eligibility_prompt.format(research_topic=topic)

    with console.status("Evaluating research eligibility...", spinner="dots"):
        result = agent.run_sync(prompt)

    return result.output

def main():
    log_initial_message()
    terminate = False

    while True:
        research_topic = Prompt.ask("\n🔬 Enter your research topic")

        if research_topic.lower() in ['quit', 'exit', 'q']:
            console.print("\n👋 Goodbye!")
            terminate = True
            break

        is_researchable = evaluate_research_eligibility(research_topic)

        if not is_researchable:
            console.print("\n🚫 Sorry, the topic is not eligible for research. Try again...", style=error_style)
            continue
        
        console.print(f"✅ Research topic \"{research_topic}\" is eligible for research!", style=success_style)
        break

    if terminate:
        return

    message_history: list[ModelMessage] = []
    is_success, initial_research_plan = create_initial_research_plan(research_topic, message_history)

    if not is_success:
        console.print("\n❌ Error creating initial plan. Exiting...", style=error_style)
        return
    
    # Start the feedback and refinement loop
    final_research_plan = finalize_plan_on_feedback(initial_research_plan, message_history)
    console.print("\n🚀 Final Research Plan:", style=success_style)
    console.print(json.dumps(final_research_plan.model_dump(), indent=2))

if __name__ == "__main__":
    main()
