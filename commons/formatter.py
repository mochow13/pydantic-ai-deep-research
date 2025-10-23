from typing import List
from commons._types import ResearchStepResult


def format_analysis(analysis: List[ResearchStepResult]) -> str:
    successful_results = [step for step in analysis if step.success]
    
    if not successful_results:
        return "ANALYSIS_EMPTY: No successful research results available."
    
    output_parts = []
    
    output_parts.append("ANALYSIS_SUMMARY:")
    
    output_parts.append("RESEARCH_STEPS:")
    for step in successful_results:
        output_parts.append(f"STEP_{step.step_number}:")
        output_parts.append(f"  TITLE: {step.title}")
        
        if step.findings:
            output_parts.append(f"  FINDINGS: {step.findings}")
        
        if step.key_insights:
            output_parts.append("  KEY_INSIGHTS:")
            for insight in step.key_insights:
                output_parts.append(f"    - {insight}")
        
        if step.sources:
            output_parts.append("  SOURCES:")
            for source in step.sources:
                output_parts.append(f"    - {source}")
        
        output_parts.append("")
    
    all_insights = []
    for step in successful_results:
        if step.key_insights:
            all_insights.extend(step.key_insights)
    
    if all_insights:
        output_parts.append("CONSOLIDATED_INSIGHTS:")
        for insight in all_insights:
            output_parts.append(f"  - {insight}")
        output_parts.append("")
    
    all_sources = []
    for step in successful_results:
        if step.sources:
            all_sources.extend(step.sources)
    
    unique_sources = []
    seen = set()
    for source in all_sources:
        if source not in seen:
            unique_sources.append(source)
            seen.add(source)
    
    if unique_sources:
        output_parts.append("ALL_SOURCES:")
        for source in unique_sources:
            output_parts.append(f"  - {source}")
    
    return "\n".join(output_parts)
