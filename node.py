from flask import Flask, jsonify,request, send_from_directory              # Web Server and converts to json and to get data and to load HTML file
from flask_cors import CORS             # Only clients running from the same server can access this server
from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
CORS(app)                               # Open up to other clients too


@app.route('/', methods=['GET'])           # Endpoint(PATH, type of request) This is for default domain
def get_node_ui():
    return send_from_directory('ui', 'node.html')

# This loads the page to manage networks
@app.route('/network', methods=['GET'])           # Endpoint(PATH, type of request) This is for default domain
def get_network_ui():
    return send_from_directory('ui', 'network.html')


@app.route('/wallet', methods=['POST'])               #Gives new public and private key
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key,port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
           'message': 'Saving the keys failed'
        }
        return jsonify(response), 500


@app.route('/wallet', methods=['GET'])                      # Gets old public and private key
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key,port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Loading the keys failed'
        }
        return jsonify(response), 500


@app.route('/balance', methods=['GET'])                     # Gets balance of user
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            'message': 'Balance fetched successfully.',
            'funds': balance
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Loading balance failed',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(response), 500


@app.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        response = {'Message': 'No data found'}
        return jsonify(response), 400
    required = ['sender',
                'recipient',
                'amount',
                'signature']
    if not all(key for key in required):
        response = {'Message': 'Some data is missing'}
        return jsonify(response), 400
    success = blockchain.add_transactions(
        values['recipient'], values['sender'], values['signature'], values['amount'], is_receiving_broadcast=True)
    if success:
        response = {
            'message': 'Successfully added transactions.',
            'transaction': {
                'sender': values['sender'],
                'recipient': values['recipient'],
                'amount': values['amount'],
                'signature': values['signature']
            }
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding transaction failed'
        }
        return jsonify(response), 500


@app.route('/broadcast-block', methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {'message': 'No data found'}
        return jsonify(response), 400
    if 'block' not in values:
        response = {'message': 'Some data is missing'}
        return jsonify(response), 400
    block = values['block']
    if block['index'] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            response = {'message': 'Block added'}
            return jsonify(response), 201
        else:
            response = {'message': 'Block seems invalid'}
            return jsonify(response), 409
    elif block['index'] > blockchain.chain[-1].index:
        response = {'message': 'Blockchain seems to differ from local blockchain'}
        blockchain.resolve_conflicts = True
        return jsonify(response), 200
    else:
        response = {'message': 'Blockchain seems to be shorter, block not added'}
        return jsonify(response), 409


@app.route('/transaction', methods=['POST'])
def add_transaction():                              #Adds a transaction to open transactions
    if wallet.public_key == None:
        response = {
            'message': 'No wallet setup'
        }
        return jsonify(response), 400
    transaction = request.get_json()                # will be a dictionary of data
    if not transaction:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    if not all(field in transaction for field in required_fields):
        response = {
            'message': 'Required data is missing '
        }
        return jsonify(response), 400
    recipient = transaction['recipient']
    amount = transaction['amount']
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transactions(recipient, wallet.public_key, signature, amount)
    if success:
        response = {
            'message': 'Successfully added transactions.',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding transaction failed'
        }
        return jsonify(response), 500


@app.route('/mine', methods = ['POST'])
def mine():
    if blockchain.resolve_conflicts:
        response = {'message': 'Resolve conflicts first, block not added'}
        return jsonify(response), 409
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
        response = {
            'message': 'Block added successfully',
            'block': dict_block,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding a block failed.',
            'wallet_setup': wallet.public_key != None
        }
        return jsonify(response), 500                   # 500 is the error


@app.route('/resolve-conflicts', methods = ['POST'])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        response = {'message': 'Chain was replaced'}
    else:
        response = {'message': 'Local chain kept'}
    return jsonify(response), 200


@app.route('/transactions', methods = ['GET'])
def get_open_transactions():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions), 200


@app.route('/chain', methods = ['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]                # convert blocks to dictionary to iterate Json
    for dict_block in dict_chain:
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
    return jsonify(dict_chain), 200


@app.route('/node', methods = ['POST'])
def add_node():
    if wallet.public_key == None:
        response = {
            'message': 'No wallet setup'
        }
        return jsonify(response), 400
    values = request.get_json()                 # Gives access to the input(request)
    if not values:
        response = {
            'message': 'No data attached'
        }
        return jsonify(response), 400
    if 'node' not in values:
        response = {
            'message': 'No node data found'
        }
        return jsonify(response), 400
    node = values.get('node')
    blockchain.add_peer_node(node)
    response = {
        'message': 'Node added successfully',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201

# This is an example to pass /node/localhost:5000
@app.route('/node/<node_url>', methods=['DELETE'])             # different cause we send the node as URL
def remove_node(node_url):
    if wallet.public_key == None:
        response = {
            'message': 'No wallet setup'
        }
        return jsonify(response), 400
    if node_url == '' or node_url == None:
        response = {
            'message': 'No Node found.'
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_url)
    response = {
        'message': 'Node removed',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200


@app.route('/nodes', methods=['GET'])
def get_nodes():
    if wallet.public_key == None:
        response = {
            'message': 'No wallet setup'
        }
        return jsonify(response), 400
    nodes = blockchain.get_peer_nodes()
    response={
        'all_nodes':nodes
    }
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)               # python node.py -p 5001
    args = parser.parse_args()
    port = args.port
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host='0.0.0.0', port=port)              # IP and port
