from console_config import console, welcome_style
from orchestrator import ResearchOrchestrator

def log_initial_message():
    console.print("🎤 Welcome to the Research Planning Assistant!", style=welcome_style)
    console.print("Please provide a research topic and I'll create a research plan for you.", style=welcome_style)
    console.print("You can then provide feedback to refine the plan until you're satisfied.", style=welcome_style)
    console.print("Type 'quit' or 'exit' to end, or 'start research' when ready to begin.", style=welcome_style)
    console.print("-" * 70, style=welcome_style)


def main():
    log_initial_message()
    orchestrator = ResearchOrchestrator()
    orchestrator.run_research_session()

if __name__ == "__main__":
    main()
