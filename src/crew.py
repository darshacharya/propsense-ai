from crewai import Crew, Process

from src.agents.researcher import get_researcher
from src.agents.analyst import get_analyst
from src.agents.investigator import get_investigator
from src.agents.reporter import get_reporter

from src.tasks.research_task import create_research_task
from src.tasks.analysis_task import create_analysis_task
from src.tasks.investigation_task import create_investigation_task
from src.tasks.report_task import create_report_task

from src.data.bangalore import format_area_for_agent


def build_crew(location: str, budget: float, user_query: str = "", task_callback=None):
    """Build the TrendIQ analysis crew.

    Args:
        location: Bangalore area name (e.g. "Whitefield")
        budget: Budget in Lakhs (e.g. 80 for ₹80L, 150 for ₹1.5Cr)
        user_query: Free-text description of the buyer's profile, goals, and concerns
        task_callback: Optional callback invoked after each task completes
    """
    market_data = format_area_for_agent(location)

    researcher = get_researcher()
    analyst = get_analyst()
    investigator = get_investigator()
    reporter = get_reporter()

    research_task = create_research_task(researcher, location, market_data, user_query)
    analysis_task = create_analysis_task(
        analyst, location, budget, research_task, user_query
    )
    investigation_task = create_investigation_task(
        investigator, location, research_task, user_query
    )
    report_task = create_report_task(
        reporter,
        location,
        budget,
        research_task,
        analysis_task,
        investigation_task,
        user_query,
    )

    kwargs = dict(
        agents=[researcher, analyst, investigator, reporter],
        tasks=[research_task, analysis_task, investigation_task, report_task],
        process=Process.sequential,
        verbose=True,
        memory=False,
    )
    if task_callback:
        kwargs["task_callback"] = task_callback

    return Crew(**kwargs)
