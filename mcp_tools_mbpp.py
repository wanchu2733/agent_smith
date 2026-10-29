from mcp.server.mcpserver import MCPServer

mcp = MCPServer("mbpp server")


@mcp.tool()
def run_tests(code: str, test_list) -> str:
    """run tests"""
    return f"good!"


if __name__ == "__main__":
    mcp.run(transport="stdio")