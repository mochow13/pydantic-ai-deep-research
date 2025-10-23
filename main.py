from dotenv import load_dotenv
from config.console_config import console, welcome_style
from deep_research.orchestrator import ResearchOrchestrator

load_dotenv()

def log_initial_message():
    console.print("🎤 Welcome to the Deep Research Assistant!", style=welcome_style)
    console.print("Please provide a research topic and I'll provide a deep research report!", style=welcome_style)
    console.print("For the research plan, you can provide feedback to refine it until you're satisfied.", style=welcome_style)
    console.print("Type 'quit' or 'exit' to end, or 'start/ok/begin' when ready to begin.", style=welcome_style)
    console.print("-" * 70, style=welcome_style)

def main():
    log_initial_message()
    orchestrator = ResearchOrchestrator()
    orchestrator.run_research_session()

if __name__ == "__main__":
    main()
