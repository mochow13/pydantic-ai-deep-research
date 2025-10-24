# Pydantic AI Deep Research

This is an AI research agent inspired by Gemini Deep Research. It conducts comprehensive research on any topic using user-provided AI models. This tool creates structured research plans, executes multi-step analysis with web search capabilities, and synthesizes findings into detailed reports.

## Overview

This research assistant leverages the `pydantic-ai` AI-agent framework and `pydantic-ai-litellm` library for using models through `litellm`. It provides:

- **Intelligent Research Planning**: Creates structured, multi-step research plans for any topic
- **Topic Eligibility**: Validates research topics for appropriateness
- **Interactive Refinement**: Allows users to provide feedback and refine research plans
- **Automated Analysis**: Executes research steps with web search integration
- **Report Synthesis**: Generates comprehensive research reports from findings

## Features

### 🤖 AI-Powered Components
- Uses multiple specialized models for different tasks:
  - GPT-4o for planning and analysis
  - GPT-4o-mini for quick eligibility checks
  - Gemini-2.5-Pro for report synthesis
- Built with `pydantic-ai` for structured AI interactions
- Integrated with `pydantic-ai-litellm` for model flexibility

### 📊 Structured Data Models
- **ResearchPlan**: Comprehensive research planning structure
- **ResearchStep**: Individual research step definitions
- **ResearchStepResult**: Detailed results with findings and sources
- Type-safe operations with Pydantic models

## Installation

### Prerequisites
- Python 3.13+
- Access to AI model APIs (configured via environment variables)

### Setup

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd pydantic-ai-deep-research
    ```

2. **Install dependencies**:
    ```bash
    # Using uv (recommended)
    uv sync

    # Or using pip
    pip install -e .
    ```

3. **Configure environment variables**:
    ```bash
    cp .env.example .env
    ```
    
    Edit `.env` file with your API credentials:
    ```
    API_BASE=your_api_base_url
    API_KEY=your_api_key
    ```

4. **Update model_config.py and put your favourite model names**
   ```python
    ANALYZER_MODEL = "<analyzer-model>"
    PLANNER_MODEL = "<planner-model>"
    PLANNER_MINI_MODEL = "<planner-mini-model>"
    SYNTHESIZER_MODEL = "<synthesizer-model>"
   ```

## Usage

### Running the Research Assistant

Start the interactive research session:

```bash
python main.py
```

### Workflow

1. **Topic Input**: Enter your research topic when prompted
2. **Plan Generation**: The system creates an initial research plan
3. **Plan Refinement**: Provide feedback to refine the plan (optional)
4. **Research Execution**: The system executes each research step with web searches
5. **Report Generation**: Comprehensive report synthesis from all findings

### Example Session

```
🎤 Welcome to the Deep Research Assistant!
Please provide a research topic and I'll provide a deep research report!

🔬 Enter your research topic: Impact of AI on modern education

✅ Research topic "Impact of AI on modern education" is eligible for research!

📜 Research Plan:

{
  "topic": "Impact of AI on modern education",
  "refined_topic": "Comprehensive analysis of AI's transformative effects on educational systems...",
  "objectives": [...],
  "key_questions": [...],
  "steps": [...]
}

💡 Your feedback on the plan (or 'start/ok/begin' to begin): start

📘 Research analysis:
[Detailed step-by-step research results...]

🔖 Final research report:
[Comprehensive synthesized report]
```

## Project Structure

```
pydantic-ai-deep-research/
├── main.py                 # Application entry point
├── pyproject.toml          # Project configuration and dependencies
├── .env.example           # Environment variables template
├── commons/               # Shared utilities and models
│   ├── _types.py          # Pydantic data models
│   ├── config.py          # Model configurations
│   ├── models.py          # Model wrapper classes
│   ├── prompts.py         # AI prompt templates
│   └── formatter.py       # Output formatting utilities
├── config/                # Configuration modules
│   └── console_config.py  # Rich console styling
└── deep_research/         # Core research modules
    ├── orchestrator.py    # Main research workflow coordinator
    ├── planner.py         # Research plan generation
    ├── analyzer.py        # Research step execution
    └── synthesizer.py     # Report synthesis
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is available under the MIT License.