from crewai import Task


def create_analysis_task(
    agent, location: str, budget: float, research_task: Task, user_query: str = ""
):
    budget_display = (
        f"₹{budget:.1f} Cr" if budget >= 100 else f"₹{budget:.0f} Lakhs"
    )

    buyer_context = ""
    if user_query.strip():
        buyer_context = f"""
BUYER'S INPUT:
\"{user_query}\"

Tailor your financial analysis to this buyer's goals. If they mention rental income,
emphasize yield. If they mention flipping, emphasize appreciation. If they mention
long-term hold, project accordingly.
"""

    return Task(
        description=f"""Based on the research brief for **{location}**, perform a detailed investment analysis.

The buyer's budget is: **{budget_display}**

{buyer_context}Your analysis must cover:

1. **Budget Fit**: Can the buyer afford a property here? What size/type is feasible within budget?
2. **Price Trend Analysis**: Is the area appreciating, stable, or declining? How does it compare to Bangalore average (+7.5% YoY)?
3. **ROI Projection**: Based on current trends, estimate 3-year and 5-year appreciation potential
4. **Rental Yield Assessment**: What rental income can the buyer expect? How does yield compare to city average (3.4%)?
5. **Value Score**: Rate the area's investment value from 1-10 considering price, trend, yield, and budget fit
6. **Buyer-Specific Assessment**: How well does this investment match what the buyer actually wants?

Be specific with numbers. Don't be vague — give precise assessments.""",
        expected_output=(
            "A detailed financial analysis covering budget feasibility, "
            "price trends, ROI projections, rental yield assessment, "
            "a value score, and buyer-specific fit assessment."
        ),
        agent=agent,
        context=[research_task],
    )
