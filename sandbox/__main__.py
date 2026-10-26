import argparse
import json
from model import SandboxConfig

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mcp-stdio", default="")
    parser.add_argument("--mcp-server", default="")
    parser.add_argument("config_file", nargs="?", default="sandbox_template.json")
    return parser.parse_args()

def load_config(path: str) -> SandboxConfig:
    with open(path, "r") as f:
        return json.load(f)

def main():
    print("sandbox main")
    args = parse_args()
    config = load_config(args.config_file)
    print(config)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
