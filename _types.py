from pydantic import BaseModel, Field
from typing import List, Optional

class ResearchStep(BaseModel):
    """A single step in the research plan"""
    step_number: int = Field(description="The sequential number of this step")
    title: str = Field(description="A concise title for this research step")
    description: str = Field(description="Detailed description of what needs to be done in this step")
    expected_outcome: str = Field(description="What should be achieved by completing this step")
    dependencies: Optional[List[int]] = Field(
        default=None, 
        description="List of step numbers that must be completed before this step"
    )

class ResearchPlan(BaseModel):
    """Complete research plan with metadata and steps for AI agent execution"""
    topic: str = Field(description="The research topic provided by the user")
    refined_topic: str = Field(description="A refined/clarified version of the research topic")
    objectives: List[str] = Field(description="Main research objectives")
    key_questions: List[str] = Field(description="Key research questions to investigate")
    steps: List[ResearchStep] = Field(description="Sequential list of research steps")
    required_resources: List[str] = Field(description="Types of resources needed (databases, tools, etc.)")