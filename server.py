from flask import Flask, render_template, jsonify
import subprocess
import json

app = Flask(__name__)

def run_core_query():
    result = subprocess.run(["python", "coreQuery.py"], capture_output=True, text=True)
    return result.stdout

@app.route('/')
def index():
    return render_template('memePoolGUI.html')

@app.route('/api/data')
def get_data():
    output = run_core_query()
    try:
        data = json.loads(output)
    except json.JSONDecodeError as e:
        return jsonify({"error": str(e)})

    if "error" in data:
        return jsonify({"error": data['error']})

    frontend_data = {
        "blockchain": {
            "chain": data["blockchain_info"]["chain"],
            "blocks": data["blockchain_info"]["blocks"],
            "bestblockhash": data["blockchain_info"]["bestblockhash"]
        },
        "mempool": {
            "txCount": data["mempool_info"]["size"],
            "mempoolSize": data["mempool_info"]["bytes"]
        },
        "latestBlock": {
            "hash": data["latest_block"]["hash"],
            "time": data["latest_block"]["time"]
        },
        "transactions": data["mempool_transactions"]
    }
    return jsonify(frontend_data)

if __name__ == '__main__':
    app.run(debug=True)