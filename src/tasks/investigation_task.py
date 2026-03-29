from crewai import Task


def create_investigation_task(
    agent, location: str, research_task: Task, user_query: str = ""
):
    buyer_context = ""
    if user_query.strip():
        buyer_context = f"""
BUYER'S INPUT:
\"{user_query}\"

Pay special attention to any concerns the buyer raised (e.g. traffic, water,
schools, safety, commute). Investigate those specific pain points in depth.
"""

    return Task(
        description=f"""Based on the research data for **{location}**, investigate the GROUND REALITY.

{buyer_context}Go beyond the numbers and explain:

1. **Why This Price?**: What factors drive the current pricing — is it genuine demand, speculative, or infrastructure-led?
2. **Livability Assessment**: What's daily life actually like here? Commute, water, power, safety, community
3. **Pain Points**: What are the top 3 problems residents face?
4. **Hidden Risks**: What could go wrong — regulatory, environmental, market-specific risks?
5. **Growth Drivers**: What specific factors could push prices up in the next 2-5 years?
6. **Who Should Buy Here**: Profile the ideal buyer (end-user vs investor, budget range, lifestyle preference)
7. **Buyer Concern Check**: Directly address each specific concern the buyer mentioned

Be honest and direct. Investors need truth, not marketing.""",
        expected_output=(
            "A ground-reality investigation covering price drivers, "
            "livability, pain points, risks, growth catalysts, ideal buyer "
            "profile, and direct answers to the buyer's specific concerns."
        ),
        agent=agent,
        context=[research_task],
    )
