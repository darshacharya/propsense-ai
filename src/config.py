import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()


def get_llm():
    if os.getenv("GEMINI_API_KEY"):
        return LLM(
            model="google/gemini-2.5-flash",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.3,
        )
    elif os.getenv("OPENAI_API_KEY"):
        return LLM(model="gpt-4o-mini", temperature=0.3)
    elif os.getenv("GROQ_API_KEY"):
        return LLM(
            model="groq/llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY"),
        )
    else:
        return LLM(
            model="ollama/llama3:8b",
            base_url="http://localhost:11434",
            temperature=0.3,
        )
