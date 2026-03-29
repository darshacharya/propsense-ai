from crewai import Task


def create_report_task(
    agent,
    location: str,
    budget: float,
    research_task: Task,
    analysis_task: Task,
    investigation_task: Task,
    user_query: str = "",
):
    budget_display = (
        f"₹{budget:.1f} Cr" if budget >= 100 else f"₹{budget:.0f} Lakhs"
    )

    buyer_context = ""
    if user_query.strip():
        buyer_context = f"""
IMPORTANT — THE BUYER SAID:
\"{user_query}\"

Your report MUST directly address this buyer's situation. The Final Recommendation
should speak to them personally — their goals, their concerns, their timeline.
Don't give generic advice. Make it specific to what they asked.
"""

    return Task(
        description=f"""You have received research, financial analysis, and ground-reality investigation for **{location}** (Budget: {budget_display}).

{buyer_context}Synthesize ALL findings into a final investment report.

Your report MUST follow this EXACT format:

---

## INVESTMENT SCORE: [X.X]/10

## VERDICT: [Good / Risky / Avoid]

## Executive Summary
[2-3 sentences capturing the key investment thesis, tailored to this buyer's needs]

## Location Overview
- Area character and vibe
- Key infrastructure highlights
- Connectivity summary

## Price & Trend Analysis
- Current price range and where it stands vs city average
- Trend direction and momentum
- Budget feasibility assessment
- 3-year and 5-year outlook

## Rental & ROI Potential
- Expected rental income
- Rental yield vs city average
- Total return projection (appreciation + rental)

## Buyer Sentiment & Livability
- What residents love
- What residents complain about
- Lifestyle fit assessment

## Risk Factors
- [List each risk as a bullet point]

## Your Concerns Addressed
- [Directly answer each concern the buyer raised, one by one]

## Final Recommendation
[3-4 sentences with a clear, decisive recommendation. Speak directly to the buyer — address their goals, timeline, and concerns. Tell them exactly what to do.]

---

SCORING GUIDE:
- 8-10: Strong Buy (Good) — solid fundamentals, good value
- 5-7.9: Conditional (Risky) — has potential but with significant caveats
- Below 5: Avoid — poor value, high risk, or fundamental issues

Be decisive. Investors pay for clarity, not hedging.""",
        expected_output=(
            "A complete investment report following the exact format specified, "
            "with investment score, verdict, all required sections, direct answers "
            "to the buyer's concerns, and a personalized recommendation."
        ),
        agent=agent,
        context=[research_task, analysis_task, investigation_task],
    )
