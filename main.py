import subprocess
import json


def run_core_query():
    # Run the coreQuery.py script and capture its output
    result = subprocess.run(["python", "coreQuery.py"], capture_output=True, text=True)
    return result.stdout


def parse_blockchain_info(output):
    # Find the start of the Blockchain Info JSON
    start = output.find("{", output.find("Blockchain Info:"))
    end = output.find("}", start) + 1
    blockchain_json = output[start:end]

    # Parse the JSON
    blockchain_info = json.loads(blockchain_json)

    # Extract the required information
    return {
        "chain": blockchain_info["chain"],
        "blocks": blockchain_info["blocks"],
        "bestblockhash": blockchain_info["bestblockhash"],
    }


def main():
    output = run_core_query()
    parsed_info = parse_blockchain_info(output)

    print("Parsed Blockchain Information:")
    print(f"- Chain: {parsed_info['chain']}")
    print(f"- Blocks: {parsed_info['blocks']}")
    print(f"- Best Block Hash: {parsed_info['bestblockhash']}")


if __name__ == "__main__":
    main()
