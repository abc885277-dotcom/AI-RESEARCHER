"""A free, no-API-key web search tool for our CrewAI agent, powered by DuckDuckGo."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from ddgs import DDGS


class DuckDuckGoSearchInput(BaseModel):
    """Input schema for the DuckDuckGo search tool."""
    query: str = Field(..., description="The search query to look up on the web.")


class DuckDuckGoSearchTool(BaseTool):
    name: str = "DuckDuckGo Web Search"
    description: str = (
        "Searches the web using DuckDuckGo and returns the top results "
        "(title, short snippet, and link) for a given query. "
        "Use this tool whenever you need current, factual, or up-to-date "
        "information that you are not certain about."
    )
    args_schema: type[BaseModel] = DuckDuckGoSearchInput
    max_results: int = 5

    def _run(self, query: str) -> str:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=self.max_results))
        except Exception as e:
            return f"Search failed for query '{query}': {e}"

        if not results:
            return f"No search results found for query: {query}"

        formatted = []
        for i, r in enumerate(results, start=1):
            title = r.get("title", "No title")
            body = r.get("body", "")
            href = r.get("href", "")
            formatted.append(f"{i}. {title}\n   {body}\n   Source: {href}")

        return "\n\n".join(formatted)
