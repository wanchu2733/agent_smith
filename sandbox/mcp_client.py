import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.streamable_http import streamable_http_client
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self):
        print("MCPClient")
        asyncio.run(
            self.get_tools_async()
        )

    def get_client(self):
        raise NotImplemented()
    
    async def get_tools_async(self):
        async with self.get_client() as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools_response = await session.list_tools()
                self.tools = tools_response.tools

    def list_tools(self):
        for tool in self.tools:
            print(f"tool.name: {tool.name}")
            print(f"tool.description: {tool.description}")
            print(f"tool.input_schema: {tool.input_schema}")


    async def call_tool_async(self, name: str, args: dict) -> list:
        async with self.get_client() as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool(name, arguments=args)
                if result.is_error:
                    print("mcp tool error")
                return result.content
                # print("\nTool Execution Result:")
                # for content in result.content:
                #     if content.type == "text":
                #         print(f"Result: {content.text}")

    def call_tool(self, name: str, args: dict) -> list:
        return asyncio.run(
            self.call_tool_async(name, args)
        )

class MCPClientStdio(MCPClient):
    def __init__(self, cmd: str):
        print("MCPClientStdio")
        command, *args = cmd.split(" ")
        self.server_params = StdioServerParameters(
            command=command,
            args=args,
        )
        super().__init__()

    def get_client(self):
        return stdio_client(self.server_params)

class MCPClientHttp(MCPClient):
    def __init__(self, url: str):
        print("MCPClientHttp")
        self.server_url = url
        super().__init__()
    
    def get_client(self):
        return streamable_http_client(self.server_url)