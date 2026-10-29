import argparse
import json
from model import SandboxConfig
from sandbox import Sandbox


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mcp-stdio", default="")
    parser.add_argument("--mcp-server", default="")
    parser.add_argument("config_file", nargs="?", default="sandbox_template.json")
    return parser.parse_args()


def load_config(path: str) -> SandboxConfig:
    with open(path, "r") as f:
        return json.load(f)


def repl(sandbox: Sandbox):
    print("repl")
    while True:
        line = input(">")
        if "exit" in line:
            break
        result = sandbox.execute(
            code=line,
            timeout=1.0,
        )
        print(f"result.stdout: {result.stdout}")
        print(f"result.stderr: {result.stderr}")
        if result.timed_out:
            print("execution timed_out")


def main():
    args = parse_args()
    config = load_config(args.config_file)
    sandbox = Sandbox(config)
    mcp_client = None
    if args.mcp_stdio:
        mcp_client = MCPClient.stdio(args.mcp_stdio)
    elif args.mcp_server:
        mcp_client = MCPClient.http(args.mcp_server)
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
