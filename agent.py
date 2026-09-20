"""Defines the single research agent, its task, and the crew that runs it."""

import os
from crewai import Agent, Task, Crew, Process, LLM
from tools.search_tool import DuckDuckGoSearchTool


def build_crew(topic: str, groq_api_key: str) -> Crew:
    # CrewAI/LiteLLM picks up the Groq key from this environment variable.
    os.environ["GROQ_API_KEY"] = groq_api_key

    llm = LLM(
        model="groq/openai/gpt-oss-120b",  # Groq's hosted OpenAI gpt-oss-120b model
        temperature=0.4,
    )

    search_tool = DuckDuckGoSearchTool()

    researcher = Agent(
        role="Senior Research Analyst",
        goal=(
            f"Research the topic '{topic}' thoroughly using web search, "
            "and produce an accurate, well-structured report."
        ),
        backstory=(
            "You are an experienced research analyst who is excellent at "
            "turning raw web search results into clear, well-organized "
            "reports. You always search for information before writing "
            "instead of relying purely on what you already know, and you "
            "note where each key fact came from."
        ),
        tools=[search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    research_task = Task(
        description=(
            f"Research the topic: '{topic}'.\n\n"
            "Steps to follow:\n"
            "1. Use the DuckDuckGo Web Search tool several times with "
            "different, specific queries to gather current information.\n"
            "2. Cross-check facts across multiple search results where possible.\n"
            "3. Write a well-structured research report in Markdown format "
            "with the following sections:\n"
            "   - A short introduction to the topic\n"
            "   - Key findings, organized under clear subheadings\n"
            "   - Relevant statistics, dates, or facts you found\n"
            "   - A brief conclusion / summary\n"
            "   - A 'Sources' section listing the links you used\n"
        ),
        expected_output=(
            "A complete Markdown-formatted research report of roughly "
            "500-800 words, with headings, a conclusion, and a sources list."
        ),
        agent=researcher,
    )

    return Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True,
    )


def run_research(topic: str, groq_api_key: str) -> str:
    """Runs the crew and returns the final report as plain text/Markdown."""
    crew = build_crew(topic, groq_api_key)
    result = crew.kickoff()
    return str(result)
