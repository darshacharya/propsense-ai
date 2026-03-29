from crewai import Task


def create_research_task(agent, location: str, market_data: str, user_query: str = ""):
    buyer_context = ""
    if user_query.strip():
        buyer_context = f"""
BUYER'S INPUT:
\"{user_query}\"

Keep this buyer's profile and concerns in mind while compiling the research.
Highlight data points that are most relevant to their specific situation.
"""

    return Task(
        description=f"""You are researching the real estate market for **{location}** in Bangalore.

{buyer_context}Here is the structured market data available for this location:

{market_data}

Your job:
1. Organize this data into a clear RESEARCH BRIEF
2. Highlight key numbers: price range, trend direction, demand level
3. List all infrastructure and connectivity factors
4. Note upcoming projects that could impact property values
5. Summarize the rental market potential
6. Flag any data points directly relevant to the buyer's stated concerns

Output a well-structured research brief that other analysts can build upon.""",
        expected_output=(
            "A structured research brief covering pricing, trends, "
            "infrastructure, connectivity, upcoming projects, and rental "
            "market for the specified Bangalore locality, with highlights "
            "relevant to the buyer's profile."
        ),
        agent=agent,
    )
