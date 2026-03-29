import argparse
from dotenv import load_dotenv

from src.crew import build_crew
from src.data.bangalore import get_all_area_names

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="TrendIQ — Bangalore Real Estate Intelligence"
    )
    parser.add_argument(
        "--location",
        type=str,
        required=True,
        help=f"Bangalore area to analyze. Options: {', '.join(get_all_area_names())}",
    )
    parser.add_argument(
        "--budget",
        type=float,
        required=True,
        help="Budget in Lakhs (e.g. 80 for ₹80L, 150 for ₹1.5Cr)",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="",
        help="Your investment goals, profile, and concerns",
    )

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  TrendIQ — Analyzing: {args.location}")
    print(f"  Budget: ₹{args.budget:.0f} Lakhs")
    if args.query:
        print(f"  Query: {args.query}")
    print(f"{'='*60}\n")

    crew = build_crew(args.location, args.budget, args.query)
    result = crew.kickoff()

    print(f"\n{'='*60}")
    print("  FINAL INVESTMENT REPORT")
    print(f"{'='*60}\n")
    print(result)


if __name__ == "__main__":
    main()
