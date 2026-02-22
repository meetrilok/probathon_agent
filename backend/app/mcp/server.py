"""MCP server exposing reusable tools for ingestion and validation workflows."""

from mcp.server.fastmcp import FastMCP

from app.core.config import get_settings

mcp = FastMCP(name="use-case-platform")


@mcp.tool()
def platform_configuration() -> dict:
    settings = get_settings()
    return {
        "vector_provider": settings.vector_provider,
        "embedding_provider": settings.embedding_provider,
        "sql_db_url": settings.sql_db_url,
        "app_env": settings.app_env,
    }


@mcp.tool()
def required_user_inputs() -> dict:
    return {
        "collecting_user_inputs": [
            "title",
            "description",
            "line_of_business",
            "source_uri(optional)",
            "contact_email(optional)",
        ],
        "exploration_inputs": ["webhook endpoint", "api documentation", "playwright harness", "repo url"],
        "infrastructure_inputs": ["runtime namespace", "database availability", "git access"],
    }


if __name__ == "__main__":
    mcp.run(transport=get_settings().mcp_transport)
