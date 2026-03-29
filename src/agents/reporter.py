from crewai import Agent
from src.config import get_llm


def get_reporter():
    return Agent(
        role="Investment Decision Reporter",
        goal=(
            "Synthesize all research, analysis, and investigation findings "
            "into a clear, actionable investment report with a definitive "
            "score, verdict, and structured reasoning."
        ),
        backstory=(
            "You are a senior investment advisor who writes final reports "
            "for high-net-worth clients. You take complex multi-source "
            "intelligence and distill it into crisp, decisive recommendations. "
            "Your reports are known for clarity — every insight is a bullet, "
            "every verdict is backed by reasoning."
        ),
        allow_delegation=False,
        llm=get_llm(),
        verbose=True,
    )
