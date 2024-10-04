import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from dotenv import load_dotenv
import os
import json
from decimal import Decimal

load_dotenv()

# Custom JSON encoder to handle Decimal objects
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

# RPC connection details
rpc_user = os.getenv("rpcUser")
rpc_password = os.getenv("rpcPassword")
rpc_host = os.getenv("rpcAddress")
rpc_port = os.getenv("rpcPort")
rpc_connection = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"

try:
    rpc_client = AuthServiceProxy(rpc_connection, timeout=120)

    # Get blockchain info
    blockchain_info = rpc_client.getblockchaininfo()

    # Get network info
    network_info = rpc_client.getnetworkinfo()

    # Get mempool info
    mempool_info = rpc_client.getmempoolinfo()

    # Get latest block info
    latest_block_hash = rpc_client.getbestblockhash()
    latest_block = rpc_client.getblock(latest_block_hash)

    # Get recent transactions from mempool
    mempool_transactions = rpc_client.getrawmempool(True)

    # Prepare output data
    output_data = {
        "blockchain_info": blockchain_info,
        "network_info": network_info,
        "mempool_info": mempool_info,
        "latest_block": latest_block,
        "mempool_transactions": mempool_transactions
    }

    # Print the output as a single JSON object
    print(json.dumps(output_data, cls=DecimalEncoder))

except JSONRPCException as json_exception:
    print(json.dumps({"error": f"A JSON RPC Exception occurred: {json_exception}"}))
except Exception as general_exception:
    print(json.dumps({"error": f"An error occurred: {general_exception}"}))