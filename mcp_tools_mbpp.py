from mcp.server.mcpserver import MCPServer
from sandbox import Sandbox

# "http://127.0.0.1:8000/mcp"
# "python lab/server_stdio.py"
mcp = MCPServer("mbpp server")

@mcp.tool()
def run_tests(code: str, test_list) -> str:
    """run tests"""
    sandbox = Sandbox()
    r = sandbox.execute(code)
    rd = dict()
    rd["success"] = False
    rd["output"] = ""
    if r.stderr:
        rd["output"] = r.stderr
        return f'{rd}'
    for test in test_list:
        r = sandbox.execute(test)
        if r.stderr:
            rd["output"] = r.stderr
            return f'{rd}'
    rd["success"] = True
    return f'{rd}'

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
