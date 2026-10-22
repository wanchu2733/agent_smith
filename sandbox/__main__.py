import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mcp-stdio", default="")
    parser.add_argument("--mcp-server", default="")
    parser.add_argument("config_file", nargs="?", default="sandbox_template.json")
    return parser.parse_args()

def main():
    args = parse_args()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
