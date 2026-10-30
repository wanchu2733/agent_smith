import argparse
import json
from mcp_client import MCPClientStdio, MCPClientHttp
from model import SandboxConfig
from sandbox import Sandbox


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mcp-stdio", default="")
    parser.add_argument("--mcp-server", default="")
    parser.add_argument("config_file", nargs="?", default="sandbox_template.json")
    return parser.parse_args()


def repl(sandbox: Sandbox):
    print("repl")
    lines = []
    while True:
        line = input(">")
        if "exit" in line:
            break
        lines.append(line)
        while True:
            line = input(">")
            if not line:
                break
            lines.append(line)
        code = "\n".join(lines)
        result = sandbox.execute(
            code=code,
            timeout=1.0,
        )
        print(f"result.stdout: {result.stdout}")
        print(f"result.stderr: {result.stderr}")
        if result.timed_out:
            print("execution timed_out")


def main():
    args = parse_args()
    sandbox = Sandbox()
    sandbox.load_config(args.config_file)
    mcp_client = None
    if args.mcp_stdio:
        mcp_client = MCPClientStdio(args.mcp_stdio)
    elif args.mcp_server:
        mcp_client = MCPClientHttp(args.mcp_server)
    if mcp_client is not None:
        sandbox.connect_mcp(mcp_client)
    repl(sandbox)
    if mcp_client is not None:
        mcp_client.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
