"""
Tavily MCP wrapper.
"""

from __future__ import annotations

from app.mcp.registry import get_tool


async def tavily_mcp_search(query: str):
    """
    Search using Tavily MCP.
    """
    tool = await get_tool("tavily", "tavily_search")
    return await tool.ainvoke({"query": query})