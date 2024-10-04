import subprocess
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import webbrowser

def run_core_query():
    result = subprocess.run(["python", "coreQuery.py"], capture_output=True, text=True)
    return result.stdout

def get_data():
    output = run_core_query()
    
    try:
        data = json.loads(output)
    except json.JSONDecodeError as e:
        return {"error": f"Error decoding JSON: {e}"}

    if "error" in data:
        return {"error": f"Error from coreQuery.py: {data['error']}"}

    return {
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

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'memePoolGUI.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = get_data()
            self.wfile.write(json.dumps(data).encode())
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Server running on http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    
    # Open the default web browser
    webbrowser.open('http://localhost:8000')
    
    # Keep the main thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down the server...")